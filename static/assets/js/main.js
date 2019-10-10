(function ($) {
    'use strict';
    $(function () {
        /*====================================
        //     Inpage Smooth Scroll
        ======================================*/
        $(document).on('click', '.ips', function (event) {
            event.preventDefault();

            $('html, body').animate({
                scrollTop: $(this.hash).offset().top
            }, 600);
        });
    });
}(jQuery));

var d = new Date();
var tuesday = new Date();
var friday = new Date();
var sunday = new Date();
var wednesday = new Date();
const saag_paneer_sku = "sku_FcuIH00wgDFDIp";
const saag_tofu_sku = "sku_FcuKuRhicxXvdf";
const saag_seitan_sku = "sku_FcuKmOkv4Zsu1A";
var delivery_sku = "";
var delivery_date;
var formvals;
const eligible_zips = ["94002", "94022", "94024", "94025", "94028", "94030", "94040", "94041", "94043", "94061", "94062", "94063", "94065", "94066", "94070", "94080", "94085", "94086", "94087", "94089", "94102", "94103", "94104", "94105", "94107", "94108", "94109", "94110", "94111", "94112", "94114", "94115", "94116", "94117", "94118", "94121", "94122", "94123", "94124", "94127", "94128", "94129", "94130", "94131", "94132", "94133", "94134", "94158", "94301", "94303", "94304", "94305", "94306", "94401", "94402", "94403", "94404", "95002", "95008", "95013", "95014", "95030", "95032", "95033", "95035", "95037", "95046", "95050","95051", "95053", "95054", "95070", "95110", "95111", "95112", "95113", "95116", "95117", "95118", "95119", "95120", "95121", "95122", "95123", "95124", "95125", "95126", "95127", "95128", "95129", "95130", "95131", "95132", "95133", "95134", "95135", "95136", "95138", "95139", "95140", "95148"];
var firebaseConfig = {
  apiKey: "AIzaSyBUMz-dcnHAE1-Hdmi34gyYa7AwbC4SsnA",
  authDomain: "pashi-signup.firebaseapp.com",
  databaseURL: "https://pashi-signup.firebaseio.com",
  projectId: "pashi-signup",
  storageBucket: "pashi-signup.appspot.com",
  messagingSenderId: "665066196308",
  appId: "1:665066196308:web:f47659b288deca3e"
};
// Initialize Cloud Firestore through Firebase
firebase.initializeApp(firebaseConfig);

var db = firebase.firestore();

var stripe = Stripe('pk_live_yYqQkXKxlqC6yrYbaIsyeVQD00zEcScs8E');

var validationOpts = {
    errorPlacement: function errorPlacement(error, element) {
      nextelem = element.next();
      if (nextelem.is('.form-text') || nextelem.is('.selectize-control')) {
        nextelem.after(error);
      } else {
        element.after(error);
      }
    },
    errorClass: "invalid-feedback",
    highlight: function(element) {
      $(element).addClass("is-invalid");
    },
    unhighlight: function(element) {
      $(element).removeClass("is-invalid");
    },
    rules: {
      phone: {
        required: true,
        phoneUS: true
      },
      email: {
        required: true,
        email: true
      },
      zip: {
        required: true,
        iseligiblezip: true
      }

    },
    messages: {
      zip: {
        required: "Please enter a Zip Code from the dropdown list"
      }
    }
};

$(document).ready(function() {
  var hash = $(location).attr('hash');
  if(hash == "#success") {
    $('.success-block').css('display','block');
  } else if (hash == "#try-again") {
    $('.failure-block').css('display','block');
  }
  $(".zero_saag").hide();
  $.each(eligible_zips, function(zip_index, single_zip) {
      // console.log(single_zip);
      $('#zip').append($('<option>', { value : single_zip }).text(single_zip));
  });
  // $('#zip').selectize({plugins: [ 'preserve_on_blur' ]});
  $('#zip').prop('required',true);
  friday.setDate(d.getDate() + (5 + 7 - d.getDay()) % 7);  // friday
  $("#friday").html($.format.date(friday.getTime(), 'MMMM D'));
  tuesday.setDate(sunday.getDate() + (2 + 7 - sunday.getDay()) % 7);  // tuesday
  $("#tuesday").html($.format.date(tuesday.getTime(), 'MMMM D'));
  // sunday.setDate(tuesday.getDate() + (7 + 7 - tuesday.getDay()) % 7);  // sunday
  d.setDate(d.getDate() + 1);
  sunday.setDate(d.getDate() + (0+(7-d.getDay())) % 7);
  $("#sunday").html($.format.date(sunday.getTime(), 'MMMM D'));
  wednesday.setDate(d.getDate() + (3 + 7 - d.getDay()) % 7);  // wednesday
  $("#wednesday").html($.format.date(wednesday.getTime(), 'MMMM D'));
  jQuery.validator.addMethod("iseligiblezip", function(value) {
    // console.log("on the road again");
    // console.log(value);
    if(value && value != 0) {
      return $.inArray(value, eligible_zips) != -1;
    }
    return false;
  }, "Please enter a Zip Code from the dropdown list");
  jQuery.validator.addMethod('phoneUS', function(phone_number, element) {
      phone_number = phone_number.replace(/\s+/g, '');
      return this.optional(element) || phone_number.length > 9 &&
          phone_number.match(/^(1-?)?(\([2-9]\d{2}\)|[2-9]\d{2})-?[2-9]\d{2}-?\d{4}$/);
  }, 'Please enter a valid phone number.');
  var form = $("#saag_order_form");
  form.validate(validationOpts);
  $( "#order_button" ).click(function() {
      form.validate().settings.ignore = ":disabled,:hidden:not(.iseligiblezip)";
      isFormValid = form.valid();
      formvals = form.serializeObject();
      console.log(formvals);
      if(formvals.delivery_time.includes('sunday')) {
        formvals.delivery_date = sunday;
        formvals.delivery_sku = "sku_FW2SIUrSf7YOg4";
      } else if(formvals.delivery_time.includes('friday')) {
        formvals.delivery_date = friday;
        formvals.delivery_sku = "sku_FW2SouIWXWGITX";
      } else if(formvals.delivery_time.includes('tuesday')) {
        formvals.delivery_date = tuesday;
        formvals.delivery_sku = "sku_FW2R4vY5OYUIH2";
      }
      saag_paneer_number = parseInt(formvals.saag_paneer_number) || 0;
      saag_tofu_number = parseInt(formvals.saag_tofu_number) || 0;
      saag_seitan_number = parseInt(formvals.saag_seitan_number) || 0;
      totalmeals = saag_paneer_number + saag_tofu_number + saag_seitan_number;
      console.log(totalmeals);
      if (totalmeals <= 0) {
        $(".zero_saag").show();
        $("html, body").animate({ scrollTop: $("#choose_saag").offset().top }, "slow");
      } else {
        $(".zero_saag").hide();
        if(isFormValid) { // form validated
          var checkoutArr = [];
          if(saag_paneer_number >= 1) {
            checkoutArr.push({sku: saag_paneer_sku, quantity: saag_paneer_number});
          }
          if(saag_tofu_number >= 1) {
            checkoutArr.push({sku: saag_tofu_sku, quantity: saag_tofu_number});
          }
          if(saag_seitan_number >= 1) {
            checkoutArr.push({sku: saag_seitan_sku, quantity: saag_seitan_number});
          }
          // if(totalmeals < 5) {
          //   checkoutArr.push({sku: formvals.delivery_sku, quantity: 1});
          // }
          db.collection("saag_orders").doc(d.toISOString()+'!'+formvals.email).set(formvals)
          .then(function() {
              console.log("Document written");
              stripe.redirectToCheckout({
                items: checkoutArr,
                customerEmail: formvals.email,

                // Do not rely on the redirect to the successUrl for fulfilling
                // purchases, customers may not always reach the success_url after
                // a successful payment.
                // Instead use one of the strategies described in
                // https://stripe.com/docs/payments/checkout/fulfillment
                successUrl: 'https://saag.pashi.com/#success',
                cancelUrl: 'https://saag.pashi.com/#try-again',
              })
              .then(function (result) {
                if (result.error) {
                  // If `redirectToCheckout` fails due to a browser or network
                  // error, display the localized error message to your customer.
                  var displayError = document.getElementById('error-message');
                  displayError.textContent = result.error.message;
                  console.log(result.error.message);
                }
              });
          })
          .catch(function(error) {
              console.error("Error adding document: ", error);
              return false;
          });
        }
      }
  });

});
