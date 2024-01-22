newCupcakeForm = $("#new-cupcake-form");
searchCupcakeForm = $("#search-cupcake-form");
cupcakesList = $("#cupcakes-list");

inputFlavor = $("#inputFlavor");
inputSearchFlavor = $("#inputSearchFlavor");
inputSize = $("#inputSize");
inputRating = $("#inputRating");
inputImgURL = $("#inputImgURL");

async function getCupcakes() {
    resp = await axios.get("/api/cupcakes");
    cupcakes = resp.data.cupcakes;

    console.log(cupcakes);

    showCupcakes(cupcakes, cupcakesList);
}

function showCupcakes(cupcakes, destination) {
    for (const cupcake of cupcakes) {
        appendCupcake(cupcake, destination);
    }
}

function appendCupcake(cupcake, destination) {
    buttonHTML = `<button class="delete-cupcake btn-sm btn-danger" data-id="${cupcake.id}">X</button>`;
    htmlString = `<b>Flavor:</b> ${cupcake.flavor} | <b>Size:</b> ${cupcake.size} | <b>Rating:</b> ${cupcake.rating} - ${buttonHTML}`;
    newListItem = $("<li>").html(htmlString);

    destination.append(newListItem);
}

function clearListItems(list) {
    list.empty();
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

async function searchFlavor(event) {
    console.log("Seaerch form submitted!");
    event.preventDefault();

    searchTerm = inputSearchFlavor.val();

    resp = await axios.get("/cupcakes/search", { params: { search_term: searchTerm } });

    cupcakes = resp.data.cupcakes;

    console.log(resp);

    clearListItems(cupcakesList);
    showCupcakes(cupcakes, cupcakesList);

    return resp;
}

async function deleteCupcake() {
    console.log("DELETE CUPCAKE");
    const id = $(this).data("id");
    await axios.delete(`/api/cupcakes/${id}`);
    $(this).parent().remove();
}

// RUN SCRIPT:
$(function () {
    $(document).on("submit", "#new-cupcake-form", createCupcake);
    $(document).on("submit", "#search-cupcake-form", searchFlavor);
    getCupcakes();
    cupcakesList.on("click", ".delete-cupcake", deleteCupcake);
});
