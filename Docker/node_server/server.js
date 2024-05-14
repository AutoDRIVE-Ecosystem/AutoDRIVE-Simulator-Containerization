const express = require('express');
const dns = require('dns');
const multer = require('multer')
const cors = require('cors');
const bodyParser = require('body-parser');

const { createProxyMiddleware } = require('http-proxy-middleware');
const { config } = require('process');

const app = express();
const port = 3000;

var database = [] // Array for storing sent metrics

// VNV Parameters
const weather_ids = [1, 2, 3, 4, 5, 6, 7, 8];
const times = [[0, 360], [720, 1080]];
const models = ["yolov2", "yolov2", "yolov2-tiny", "yolov2-tiny", "yolov3", "yolov3", "yolov3-tiny", "yolov3-tiny"]

// Stress Test / Constant Condition Parameters
// Weather ids: [0=Custom, 1=Sunny, 2=Cloudy, 3=LightFog, 4=HeavyFog, 5=LightRain, 6=HeavyRain, 7=LightSnow, 8=HeavySnow]

// Stress Test Parameters
// const weather_ids = [1, 1, 1, 1, 1, 1, 1, 1];
// const times = [560, 560];
// const models = ["yolov3"];

// Simulation Condition selection parameter needed
// Iterate through times[0-1] and model[0-4] for 8 conditions

var counter = 0;

var config_arr = []

app.use(cors());

// Use middleware to parse JSON and URL-encoded data
app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));

// Not sure why this isn't working --> keep getting error saying I am missing a target option.

// const dynamicProxy = createProxyMiddleware((req) => {
//     const options = { target: req.query.address }
//     return options;
// });

var simultation_condition_iter = 0;

/**
 * Endpoint: Handles a POST request to iterate through simulation conditions.
 * 
 * Upon receiving a request, this endpoint generates new configurations based on predefined weather IDs, times, and models arrays.
 * The variable 'simulation_condition_iter' is incremented to keep track of the iteration count, and configurations are updated accordingly.
 * 
 * Currently there exist issues when using a time, model, or condition array of size 1
 * 
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Object} JSON response indicating the successful iteration of simulation conditions.
 */
app.post('/iterate_simulation_conditions', (req, res) => {

    // generate new configs with new variables & update config_arr
    simultation_condition_iter++;
    config_arr = generate_config(weather_ids, times[simultation_condition_iter % times.length], models[simultation_condition_iter % models.length]);
    console.log("Iterated simulation conditions to: Time=" + times[simultation_condition_iter % times.length] + " and model = " +  models[simultation_condition_iter % models.length]);

    res.json("Stored simulation conditions iterated.");

});

/**
 * Function: Perform a DNS lookup using the dns module and return the results
 * 
 * This function is used to discover a list of IP addresses for all pods behind
 * the cluster's headless service. The IPs are used to load hls streams & collect data.
 * 
 * @param {Object} domain The domain to perform a Dns lookup for
 * @returns {Promise} Promise containing the resulting addresses for the dns lookup
 */
function performDnsLookup(domain) {

    // Return all IPs behind a given domain
    const options = {
        all: true
    }

    return new Promise((resolve, reject) => {
        dns.lookup(domain, options, (err, address) => {
            if (err) {
                console.log(err)
                return reject([]);
            }
            return resolve(address)
        })
    })

}

// Global variable for holding array of pod ip addresses
var podips

/**
 * Function: Generate a config from given weather, time and model arrays
 * 
 * This builds the configuration data to be sent to each pod based on pre-defined arrays
 * 
 * TODO: this function is buggy, come up with a more robust approach.
 * 
 * @param {Array} weathers Array of weather conditions
 * @param {Array} times Array of times 
 * @param {Array} model Model to be used in the simulation
 * @returns {Array} Resulting 2d array of dictionaries containing config info
 */
function generate_config(weathers, times, model) {

    config_arr = []

    for (let i = 0; i < weathers.length; i++) {
        for (let j = 0; j < times.length; j++) {
            //console.log("parsing: time:" + times[j] + " weather: " + weathers[i] + " model: " + model)
            config_arr.push({"time": times[j], "weather": weathers[i], "model": model});
        }
    }

    console.log("Generated config.");
    print_config(config_arr)
    return config_arr

}

/**
 * Function: Helper function to print a generated config for debugging
 * 
 * @param {Array} config_arr Config array which is printed
 */
function print_config(config_arr) {
    for(let i = 0; i < config_arr.length; i++) {
        console.log("time: " + config_arr[i]["time"] + " weather_id: " + config_arr[i]["weather"] + " model: " + config_arr[i]["model"])
    }
}

/**
 * Function: Function to initialize server global variables & dynamic proxy for streams
 * 
 * This function is called to start server listening & set up a dynamic proxy so that
 * video streams can be forwarded to the frontend with dynamic pod ip addresses.
 * 
 * Currently a pod's position on the list of IP addresses is determined by a race condition,
 * this causes pods to shift video streams on the frontend if streams are refreshed. In the
 * future this should be made consistent so metrics can be reported directly to the frontend.
 * 
 * @param {Object} address List of current pod IP addresses.
 */
async function server_init(address) {

    podips = address;
    console.log("podips: " + podips);

    config_arr = await generate_config(weather_ids, times, models[0]);

    /**
     * Endpoint: Proxy endpoint to request a pod hls stream.
     * 
     * Pod IP's are abstracted & pods are instead referenced by their index in the pod IP array.
     */
    app.use('/stream', function(req, res, next) {
    
        // debug statements
        // console.log("forwarding stream request to: http://" + podips[parseInt(req.url.split('/')[1])] + ":8000")
        // if(true){
        //     console.log(req.url)
        //     console.log(podips[0].address)
        //     console.log(req.url.split('/'))
        // }

        var podnumber = req.url.split('/')[1];
        console.log("processing reques for pod number " + podnumber + "at ip " + podips[parseInt(req.url.split('/')[1])].address + "from url " + req.url)
        createProxyMiddleware({
            target: "http://" + podips[parseInt(req.url.split('/')[1])].address + ":8000",
            pathRewrite: function (path, req) { return path.replace('/stream/'+podnumber, '') },
            changeOrigin: true
        })(req, res, next);
    
    });

    // Listen on port
    app.listen(port, () => {
        console.log(`Server listening at http://localhost:${port}`);
    });

}

/**
 * Endpoint: GET request to send current configuration conditions when spinning up new simulations.
 * 
 * The logging library inside each simulation pod calls this endpoint to grab current simulation conditions from
 * the server. 
 * 
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Object} JSON response containing the next simulation condition in rotation.
 */
app.get('/variabilityconfig', (req, res) => {

    counter++;
    console.log("config request: " + counter);
    // res.json({ "config": config_arr[ counter % podips.length ]});
    res.json({ "config": config_arr[ counter % config_arr.length ]});

});

/**
 * Endpoint: GET request for a dns lookup
 * 
 * This endpoint is used to retrieve pod IPs using the performDnsLookup() function.
 * Currently the domain is set to sim-gateway to match the configured headless service.
 * 
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Object} List of IP addresses behind a given domain
 */
app.get('/dns-lookup', (req, res) => {
    const domain = "sim-gateway";

    if (!domain) {
        return res.status(400).json({ error: 'Domain parameter is required' });
    }

    console.log('Looking up ', domain)
    performDnsLookup(domain)
        .then(result => {
            res.json(result);
            // pod_ips = result;
        })
        .catch(error => {
            console.error('Error performing DNS lookup:', error);
            res.status(500).json({ error: 'Internal Server Error' });
        });
});

/**
 * Endpoint: GET Request to send current database of simulation data.
 * 
 * Host the dictionary database of collected simulation data so that it can be sent
 * outside of the cluster.
 * 
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Object} Server simulation database.
 */
app.get('/collectdata', (req, res) => {

    console.log("Sending data from server...");
    res.json(data=database);

});


/**
 * Endpoint: POST endpoint to receive simulation data from pods after a simulation has finished.
 * 
 * Saves simulation data from the request into the database array. 
 * 
 * @param {Object} req - The request object containing simulation data.
 * @param {Object} res - The response object.
 * @returns {Object} Returns confirmation of metric data being received.
 */
app.post('/database', (req, res) => {

    var metric_data = req.body.data;

    if (!metric_data) {
        return res.status(400).send('No data found.');
    }

    console.log("Metric Data received: \n");
    database.push(metric_data);

    res.send('Metrics received.');
  });


/**
 * Endpoint: Handles a POST request to reset current server database
 * 
 * This endpoint is called by the automation module in between simulation batches
 * to dump data that has already been sent outside the cluster.
 * 
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Object} Confirmation of database reset.
 */
app.post('/resetdatabase', (req, res) => {
    
    console.log("Resetting Database")
    database = []
    res.json("Database Reset.")

})

/**
 * Endpoint: Handles a POST request to reset stored POD IP addresses.
 * 
 * Endpoint called by the frontend in order to re load saved pod IP addresses and
 * refresh hls streams.
 * 
 * @param {Object} req - The request object.
 * @param {Object} res - The response object.
 * @returns {Object} Confirmation of reset.
 */
app.post('/reset', (req, res) => {

    console.log("Resetting stored video streams...")

    // reset server side IPs
    var newPromise = performDnsLookup("sim-gateway")

    newPromise.then(
        function(address) {podips=address; console.log(podips); res.json({"reset": true})},
        function(error) {console.log(error); res.json({"reset": false});}
    )

});

// Promise used to lookup pod IP addresses
const podipsPromise = performDnsLookup("sim-gateway")
podipsPromise.then(
    function(address) {server_init(address);},
    function(error) {console.log(error);server_init([]);}
);
