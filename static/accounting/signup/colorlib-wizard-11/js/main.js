(function ($) {

    var form = $("#signup-form");
    form.validate({
        errorPlacement: function errorPlacement(error, element) {
            element.before(error);
        },
        rules: {
            national_id: {
                required: true,
            },
            gender: {
                required: true,
            },
            father_name: {
                required: true,
            },
            birth_date: {
                required: true,
            },
            birth_month: {
                required: true,
            },
            birth_year: {
                required: true,
            },
            password1: {
                required: true,
            },
            password2: {
                required: true,
            },
            first_name: {
                required: true,
            },
            last_name: {
                required: true,
            },
            user_name: {
                required: true,
            },
            password: {
                required: true,
            },
            email: {
                required: true,
            },
            phone_number: {
                required: true,
            },
            caravan: {
                required: true,
            },
            college: {
                required: true,
            },
        },
        onfocusout: function (element) {
            $(element).valid();
        },
        highlight: function (element, errorClass, validClass) {
            $(element.form).find('.actions').addClass('form-error');
            $(element).removeClass('valid');
            $(element).addClass('error');
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element.form).find('.actions').removeClass('form-error');
            $(element).removeClass('error');
            $(element).addClass('valid');
        }
    });
    form.steps({
        headerTag: "h3",
        bodyTag: "fieldset",
        transitionEffect: "fade",
        labels: {
            previous: 'قبلی',
            next: 'بعدی',
            finish: 'ثبت نام',
            current: ''
        },
        titleTemplate: '<span class="title">#title#</span>',
        onStepChanging: function (event, currentIndex, newIndex) {
            form.validate().settings.ignore = ":disabled,:hidden";
            return form.valid();
        },
        onFinishing: function (event, currentIndex) {
            // form.validate().settings.ignore = ":disabled";
            return form.valid();
        },
        onFinished: function (event, currentIndex) {
            // this function call when finish called
            var object = {};
            formData = new FormData(document.forms[0]);
            formData.forEach(function (value, key) {
                object[key] = value;
            });
            object['csrfmiddlewaretoken'] = window.csrf;
            var json = JSON.stringify(object);

            $.ajax({
                type: 'POST',
                url: window.destination_address,
                data: object,
                success: function (json) {

                    Swal.fire({
                        title: 'ثبت نام شما موفق آمیز بود',
                        text: "کد فعال سازی برای شما ارسال شد",
                        icon: 'success',
                        confirmButtonColor: '#41d639',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'فعال سازی'
                    }).then((result) => {
                        let activate_address = location.origin + '/accounting/activate';
                        console.log(activate_address);
                        location.replace(activate_address);
                    });

                },
                error: function (xhr, errmsg, err) {
                    console.log(xhr);
                    Swal.fire(
                        'اطلاعات غلط',
                        xhr.responseText,
                        'error'
                    );
                }
            });

        },
        // onInit : function (event, currentIndex) {
        //     event.append('demo');
        // }
    });

    jQuery.extend(jQuery.validator.messages, {
        required: "",
        remote: "",
        email: "",
        url: "",
        date: "",
        dateISO: "",
        number: "",
        digits: "",
        creditcard: "",
        equalTo: ""
    });


    $.dobPicker({
        daySelector: '#birth_date',
        monthSelector: '#birth_month',
        yearSelector: '#birth_year',
        dayDefault: 'روز',
        monthDefault: 'ماه',
        yearDefault: 'سال',
        minimumAge: 0,
        maximumAge: 120
    });


})(jQuery);