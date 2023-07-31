// array of work form ids
const workFormArray = [
  "#id_get_ready_time",
  "#id_commute_time",
  "#id_work_time_from",
  "#id_work_time_to",
];

// if checkbox ticked, workform appears with all required fields, else wake up with one required field
$(document).ready(function () {
  $("#toggleForm").on("change", function () {
    if ($(this).is(":checked")) {
      if ($("#id_wake_time").is(":required")) {
        $("#id_wake_time").removeAttr("required");
        $("#id_wake_time").val('');
      }
      $("#wakeUpTimeGroup").slideUp();
      $("#workForm").slideDown();
      for (let formElement of workFormArray) {
        if (!$(formElement).is(":required")) {
          $(formElement).attr("required", "required");
        }
      }
    } else {
      for (let formElement of workFormArray) {
        if ($(formElement).is(":required")) {
          $(formElement).removeAttr("required");
          $(formElement).val('');
        }
      }
      $("#workForm").slideUp();
      $("#wakeUpTimeGroup").slideDown();
      if (!$("#id_wake_time").is(":required")) {
        $("#id_wake_time").attr("required", "required");
      }
    }
  });
});

