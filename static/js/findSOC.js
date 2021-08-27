function analyticsToggle() {
  var x = document.getElementById("analytics");
  
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
  console.log('analyticsToggle')
  var jd = document.getElementById("jd").innerHTML;
  document.getElementById('jd').value = jd;
  console.log(jd)
}

/*var findSoc = document.getElementById( "findSOC" );
var socSubmit = document.getElementById( "analytics" );
console.log('findSoc : ', findSoc)
console.log('socSubmit : ', socSubmit)
findSoc.addEventListener( "click", function( event ) {
    var message = document.querySelector( '.job-message' );
    var hiddenDiv = document.querySelector( '.select-suggestion' );
    var errorElement = document.querySelector( ".alert-message" );
    console.log('message : ', message)
    console.log('hiddenDiv : ', hiddenDiv)
    console.log('errorElement : ', errorElement)
    if ( message && message.value != '' ) {
    	errorElement.classList.remove( 'alert-error' );
    	errorElement.classList.remove( 'alert-success' );
    	errorElement.classList.remove( 'show-notice' );
        hiddenDiv.classList.remove( 'soc-hidden' );
    } else {
    	document.getElementById( 'error-notice-text' ).innerHTML = 'Please enter job description';
    	errorElement.classList.remove( 'alert-success' );
		errorElement.classList.add( 'alert-error' );
		errorElement.classList.add( 'show-notice' );
		socSubmit.reset();
        hiddenDiv.classList.add( 'soc-hidden' );
    }  
} );*/  
 
   /*window.onload = function () { // when page loads

    document.getElementById('socform').onsubmit=function() {
      return confirm(document.getElementById('radio_1').checked || document.getElementById('radio_2').checked ||
      document.getElementById('radio_3').checked || document.getElementById('radio_4').checked ||
      document.getElementById('radio_5').checked || document.getElementById('radio_6').checked ? 
        "Local Pickup?" : 
        "Delivery from 536 S College Ave, Chicago, IL?");
    }    
  }*/

  /*window.onload = function () { // when page loads

    document.getElementById('socform').onsubmit=function() {
      return confirm(document.getElementById('radio_1').checked || document.getElementById('radio_2').checked || 
      document.getElementById('radio_3').checked || document.getElementById('radio_4').checked? 
        "S1" : 
        "S2");
    }    
  }*/
  /*window.onload = function () { // when page loads
    var rad1 = document.getElementById('radio_1')
    var rad2 = document.getElementById('radio_2')
    var rad3 = document.getElementById('radio_3')
    var rad4 = document.getElementById('radio_4')
    var rad5 = document.getElementById('radio_5')
    var rad6 = document.getElementById('radio_6')
    if(rad4 == null){rad4 = 'rad4'}

    console.log('rad1 : ', rad1)
    console.log('rad4 : ', rad4)
    document.getElementById('socform').onsubmit=function() {
      return confirm(document.getElementById('radio_1').checked || document.getElementById('radio_4').checked? 
        "S1" : 
        "S2");
    }    
  }*/

/*console.log('here')

$(document.getElementById('socform')).on("change", function() {
  validate();
});

function validate() {
   var valid = true;
   console.log('Here')
   if(!$('[name="radio_1"]:checked').val()) {
      valid = false;
      console.log('True')

   }
   if(!$('[name="suggestions"]').prop('checked')) {
      valid = false;
   }
 console.log('valid : ', valid)
   $('input[type="submit"]').prop("disabled", !valid)
}*/