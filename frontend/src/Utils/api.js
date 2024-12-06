//const BASE = "http://test.api.brickify.art"; //make this an evironment variable
// const BASE = "http://127.0.0.1:5000";
const BASE = "http://test.api.brickify.art";

/**
 * 
 * @param {*} method 
 * @param {*} endpoint 
 * @param {*} query 
 * @param {*} body 
 * @returns 
 */
async function request(method, endpoint, query, body) {
    let url = BASE + endpoint;

    const requestData = {
        method : method,
        mode: "cors", 
        headers: {"Content-Type" : "application/json"},
        referrerPolicy: "no-referrer", 
        cache: "default" // remove this later and have it do default caching (also maybe set up authorization?)
    };

    //add query params if necessary
    if (query != null) {
        url += "?" + new URLSearchParams(query)
    }

    if (body != null) {
        requestData.body = JSON.stringify(body);
    }

    const resp = await fetch(url, requestData);
    const data = await resp.json();
    return [resp.status, data]
}


async function getMosaic() {

}


async function getPiecelist() {
    
}

export default request;