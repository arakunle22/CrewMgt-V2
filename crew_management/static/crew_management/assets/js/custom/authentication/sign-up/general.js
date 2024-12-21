"use strict";

var KTSignupGeneral = function () {
    var form, submitButton, validation, passwordMeter;

    return {
        init: function () {
            // Form and Submit Button Elements
            form = document.querySelector("#kt_sign_up_form");
            submitButton = document.querySelector("#kt_sign_up_submit");

            // Password Strength Meter
            passwordMeter = KTPasswordMeter.getInstance(form.querySelector('[data-kt-password-meter="true"]'));

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
                        email: {
                            validators: {
                                notEmpty: {
                                    message: "Email address is required"
                                },
                                emailAddress: {
                                    message: "The value is not a valid email address"
                                }
                            }
                        },
                        password1: {
                            validators: {
                                notEmpty: {
                                    message: "The password is required"
                                },
                                callback: {
                                    message: "Please enter a valid password",
                                    callback: function (input) {
                                        if (input.value.length > 0) {
                                            return passwordMeter.getScore() > 50;
                                        }
                                        return true;
                                    }
                                }
                            }
                        },
                        password2: {
                            validators: {
                                notEmpty: {
                                    message: "The password confirmation is required"
                                },
                                identical: {
                                    compare: function () {
                                        return form.querySelector('[name="password1"]').value;
                                    },
                                    message: "The password and its confirmation are not the same"
                                }
                            }
                        },
                        toc: {
                            validators: {
                                notEmpty: {
                                    message: "You must accept the terms and conditions"
                                }
                            }
                        }
                    },
                    plugins: {
                        trigger: new FormValidation.plugins.Trigger({
                            event: {
                                password: false
                            }
                        }),
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

            // Handle password input
            form.querySelector('input[name="password1"]').addEventListener("input", function () {
                if (this.value.length > 0) {
                    validation.updateFieldStatus("password1", "NotValidated");
                }
            });
        }
    };
}();

// Initialize the script on document ready
KTUtil.onDOMContentLoaded(function () {
    KTSignupGeneral.init();
});

