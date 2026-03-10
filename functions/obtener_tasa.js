const axios = require('axios');

exports.handler = async (event, context) => {
    const MARGEN_ACADEMIA = 20.00;
    const fuentes = [
        "https://open.er-api.com/v6/latest/USD",
        "https://pydolarvenezuela-api.vercel.app/api/v1/dollar/page?page=bcv"
    ];

    let tasa_final = 45.00 + MARGEN_ACADEMIA; // Fallback
    let status = "fallback";

    for (const url of fuentes) {
        try {
            const response = await axios.get(url, { timeout: 4000 });
            let tasa_base = 0;

            if (response.data.rates) { // API Internacional
                tasa_base = response.data.rates.VES;
            } else if (response.data.monitors) { // PyDolar
                tasa_base = response.data.monitors.usd.price;
            }

            if (tasa_base > 0) {
                tasa_final = Number((tasa_base + MARGEN_ACADEMIA).toFixed(2));
                status = "success";
                break;
            }
        } catch (error) {
            continue;
        }
    }

    return {
        statusCode: 200,
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({ tasa: tasa_final, status: status })
    };
};