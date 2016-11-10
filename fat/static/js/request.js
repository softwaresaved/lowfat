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
        newBudget += Number(document.getElementById(budget_id).value);
    }


    document.getElementById("id_total_budget").value = newBudget;
}
