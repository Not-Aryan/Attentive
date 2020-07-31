// var CLIENT_ID = '229846019023-4ffjj2kv3qmkk6ecb3unfp87amhj6c98.apps.googleusercontent.com';
// var API_KEY = 'AIzaSyCvDjA8icffmXu77w_ASDQA4OvYfm0UKCM';

var API_KEY = "AIzaSyCgE9A8a2k_NB8XNvvEBkV_Enf1TdzBUxY";
var CLIENT_ID = "1037786606011-mfuqk1j4fhb52vsdbs58ne4f1he85q11.apps.googleusercontent.com";

var DISCOVERY_DOCS = ["https://www.googleapis.com/discovery/v1/apis/classroom/v1/rest"];

var SCOPES = "https://www.googleapis.com/auth/classroom.courses.readonly https://www.googleapis.com/auth/classroom.coursework.me.readonly https://www.googleapis.com/auth/classroom.profile.photos https://www.googleapis.com/auth/classroom.profile.emails";

var authorizeButton = document.getElementById('authorize_button');
var signoutButton = document.getElementById('signout_button');

function handleClientLoad() {
  gapi.load('client:auth2', initClient);
}

function initClient() {
  gapi.client.init({
    apiKey: API_KEY,
    clientId: CLIENT_ID,
    discoveryDocs: DISCOVERY_DOCS,
    scope: SCOPES
  }).then(function () {
    gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);
    updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
    authorizeButton.onclick = handleAuthClick;
    signoutButton.onclick = handleSignoutClick;
  }, function(error) {
    alert("ERROR");
    // appendPre(JSON.stringify(error, null, 2));
  });
}

function updateSigninStatus(isSignedIn) {
  if (isSignedIn) {
    mainPageTrans();
    // listCourses();
    // listCoursework();
    // getPFP();
  } else {
    alert("SAME SAME");
  }
}

function handleAuthClick(event) {
  gapi.auth2.getAuthInstance().signIn();
}

function handleSignoutClick(event) {
  gapi.auth2.getAuthInstance().signOut();
}


function mainPageTrans() {
  console.log("HERE");
  var modal = document.querySelector(".start-modal");
  var main = document.querySelector(".main-container");
  modal.style.display = "none";
  main.style.display = "block";
  getPFP();
  listCourses();
  // change();
}

function listCourses() {
  gapi.client.classroom.courses.list({
    pageSize: 10
  }).then(function(response) {
    var courses = response.result.courses;
    if (courses.length > 0) {
      for (i = 0; i < courses.length; i++) {
        var course = courses[i];
        console.log(course.name);
        let option = `<option value="${course.id}">${course.name}</option>`;
        $("#classes").append(option);
        // appendPre(course.name);
        console.log(course.id);
      }
    } else {
      let option = `<option value="no-course">No courses</option>`;
      $("#classes").append(option);
    }
  });
}

$('#classes').change(function () {
  console.log("HERE");
  $('#assignments').empty();
  var value = $(this).find('option:selected').text();
  var id = $(this).find('option:selected').val();
  if (value != "No courses"){
    gapi.client.classroom.courses.courseWork.list({
      "courseId": id
    }).then(function(response) {
      var data = response.result.courseWork;
      console.log(data)
      // appendPre1('Course Work:');
  
      if (data.length > 0 && data.length >= 5) {
        for (i = 0; i < 5; i++) {
          var course = data[i];
          let option = `<option value="${course.title}">${course.title}</option>`;
          $("#assignments").append(option);
        }
      } else {
        let option = `<option value="no-assignments">No assignments</option>`;
        $("#assignments").append(option);
        // appendPre1('No courses found.');
      }
    });
  }
});

function getPFP() {
  var current = gapi.auth2.getAuthInstance().currentUser.get().getBasicProfile();
  console.log(current.getGivenName());
  document.querySelector(".logo").innerHTML = "Hi " + current.getGivenName() + "!";
  document.querySelector("#PFP").src = "" + current.getImageUrl() + "";
  console.log(current.getImageUrl());
  console.log(current.getEmail());
}


function change() {
  var current = gapi.auth2.getAuthInstance().currentUser.get().getBasicProfile();
  var list = {};
  list.name = current.getName();
  list.class = $('#classes').find('option:selected').text();
  list.assign = $('#assignments').find('option:selected').text();

  if (document.querySelector(".start").innerHTML == "Start"){
      document.querySelector(".start").innerHTML = "End";
      $.ajax({
          type: "POST",
          url: "http://127.0.0.1:8000/startimg",
          data: JSON.stringify(list),
          dataType: 'json'
      }).done(function() {
          console.log("DONE");
      });
  }
  else if (document.querySelector(".start").innerHTML === "End") {
      document.querySelector(".start").innerHTML = "Ended";
      countdown = setInterval(function(){
          document.querySelector(".start").innerHTML = "Start";
          clearInterval(countdown)
      }, 1000);
      $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/stopimg",
        data: JSON.stringify(list),
        dataType: 'json'
      }).done(function() {
          console.log("DONE");
      });
  }
}



// document.querySelector(".startbtn").addEventListener('click', function() {
//   alert("HERE");
//   if (document.querySelector(".start").value === "Start"){
//       document.querySelector(".start").value = "End";
//   }
//   else if (document.querySelector(".start").value === "End") {
//       document.querySelector(".start").value = "Ended";
//       countdown = setInterval(function(){
//           document.querySelector(".start").value = "End";
//           clearInterval(coutndown)
//       }, 1000);
//   }
// });


