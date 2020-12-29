exports.handler = function (event, context) {
    const spawn = require("child_process").spawn;

    //console.log(event, context)
    //console.log("Event: ", event)
    // console.log("====================")
    // console.log("Context: ", context)
    // console.log("====================")
    // console.log("====================")
    // console.log("====================")
    // console.log('print ', `Hello ${JSON.parse(event.body).payload.name}`)
    const pythonProcess = spawn('python',["print", `Hello ${JSON.parse(event.body).payload.name}`]);
    console.log(pythonProcess)
    return {
        statusCode: 200,
        body: `Response: ${pythonProcess}`
    }
}