$(document).ready(function () {
  $("#toggleForm").on("change", function () {
    if ($(this).is(":checked")) {
      $("#workForm").slideDown();
      $("#wakeUpTimeGroup").slideUp();
    } else {
      $("#workForm").slideUp();
      $("#wakeUpTimeGroup").slideDown();
    }
  });
});
