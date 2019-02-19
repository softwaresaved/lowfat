/* Javascript for Request form. */

/* Calculate total budget request. */
update_budget = function() {
    var newBudget = 0
    var budgetFields = ["id_budget_request_travel",
                        "id_budget_request_attendance_fees",
                        "id_budget_request_subsistence_cost",
                        "id_budget_request_venue_hire",
                        "id_budget_request_catering",
                        "id_budget_request_others"];

    for (var budget_id of budgetFields) {
        var item = document.getElementById(budget_id);
        item.value = parseFloat(item.value).toFixed(2);
        newBudget += Number(document.getElementById(budget_id).value);
    }

    document.getElementById("id_total_budget").value = newBudget.toFixed(2);
}

document.addEventListener('DOMContentLoaded', function() {
   update_budget()
}, false);

/* Hide some costs input */
update_cost_list = function() {
    var category = document.getElementById("id_category");
    var venue = document.getElementById("div_id_budget_request_venue_hire");
    var catering = document.getElementById("div_id_budget_request_catering");
    if (category.value == "A") {
        venue.style.display = "none";
        catering.style.display = "none";
    }
    if (category.value == "H") {
        venue.style.display = "block";
        catering.style.display = "block";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var category = document.getElementById("id_category");
    category.onchange = update_cost_list;
});
