"use strict";

var KTSigninGeneral = function () {
    var form, submitButton, validation;

    return {
        init: function () {
            // Form and Submit Button Elements
            form = document.querySelector("#kt_sign_in_form");
            submitButton = document.querySelector("#kt_sign_in_submit");

            // Form Validation
            validation = FormValidation.formValidation(
                form,
                {
                    fields: {
                        username: {
                            validators: {
                                notEmpty: {
                                    message: "Username is required"
                                }
                            }
                        },
                        password: {
                            validators: {
                                notEmpty: {
                                    message: "Password is required"
                                }
                            }
                        }
                    },
                    plugins: {
                        trigger: new FormValidation.plugins.Trigger(),
                        bootstrap: new FormValidation.plugins.Bootstrap5({
                            rowSelector: ".fv-row",
                            eleInvalidClass: "",
                            eleValidClass: ""
                        })
                    }
                }
            );

            // Submit Button Handler
            submitButton.addEventListener("click", function (e) {
                e.preventDefault();

                // Validate the form
                validation.validate().then(function (status) {
                    if (status === "Valid") {
                        // Add loading indicator
                        submitButton.setAttribute("data-kt-indicator", "on");
                        submitButton.disabled = true;

                        // Allow Django to handle the authentication process
                        form.submit();
                    } else {
                        Swal.fire({
                            text: "Please fill in all required fields correctly.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }
                });
            });
        }
    };
}();

// Initialize the script on document ready
KTUtil.onDOMContentLoaded(function () {
    KTSigninGeneral.init();
});
