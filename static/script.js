newCupcakeForm = $("#new-cupcake-form");
cupcakesList = $("#cupcakes-list");

inputFlavor = $("#inputFlavor");
inputSize = $("#inputSize");
inputRating = $("#inputRating");
inputImgURL = $("#inputImgURL");

function appendCupcake(cupcake, destination) {
    console.log("Todo: add cupcake to list.");
}

async function createCupcake(event) {
    console.log("Form submitted!");
    event.preventDefault();

    newCupcake = {
        flavor: inputFlavor.val(),
        size: inputSize.val(),
        rating: inputRating.val(),
        image_url: inputImgURL.val(),
    };

    resp = await axios.post("/api/cupcakes", newCupcake);

    console.log(resp);

    appendCupcake(newCupcake, cupcakesList);

    return resp;
}

$(document).on("submit", "#new-cupcake-form", createCupcake);
