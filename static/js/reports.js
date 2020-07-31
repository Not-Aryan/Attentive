// var CLIENT_ID = '229846019023-4ffjj2kv3qmkk6ecb3unfp87amhj6c98.apps.googleusercontent.com';
// var API_KEY = 'AIzaSyCvDjA8icffmXu77w_ASDQA4OvYfm0UKCM';

var API_KEY = "AIzaSyCgE9A8a2k_NB8XNvvEBkV_Enf1TdzBUxY";
var CLIENT_ID = "1037786606011-mfuqk1j4fhb52vsdbs58ne4f1he85q11.apps.googleusercontent.com";

var DISCOVERY_DOCS = ["https://www.googleapis.com/discovery/v1/apis/classroom/v1/rest"];

var SCOPES = "https://www.googleapis.com/auth/classroom.courses.readonly https://www.googleapis.com/auth/classroom.coursework.me.readonly https://www.googleapis.com/auth/classroom.profile.photos https://www.googleapis.com/auth/classroom.profile.emails https://www.googleapis.com/auth/classroom.rosters.readonly https://www.googleapis.com/auth/classroom.coursework.students.readonly";

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
    appendPre(JSON.stringify(error, null, 2));
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
    gapi.client.classroom.courses.teachers.list({
      "courseId": id
    }).then(function(response) {
      var email = response.result.teachers[0].profile.emailAddress;
      var current = gapi.auth2.getAuthInstance().currentUser.get().getBasicProfile();
      if (current.getEmail() === email) {
          getAssignments(true, id);
      }
      else {
        getAssignments(false, id);
      }
    });
  }
});

function getAssignments(okay, id) {
    if (okay){
        gapi.client.classroom.courses.courseWork.list({
            "courseId": id
        }).then(function(response) {
            var data = response.result.courseWork;
            console.log(data);
            for (i=0;i<data.length;i++){
                var course = data[i];
                let option = `<option value="${course.title}">${course.title}</option>`;
                $("#assignments").append(option);
            }
            // if (data.length > 0 && data.length >= 5) {
            //   for (i = 0; i < 5; i++) {
                // var course = data[i];
            //     let option = `<option value="${course.title}">${course.title}</option>`;
            //     $("#assignments").append(option);
            //   }
            // } else {
            //     alert("TOO LITTLE");
            //   // appendPre1('No courses found.');
            // }
          });

    }
    else {
        let option = `<option value="no-assignments">It seems that you're not the teacher of this course</option>`;
        $("#assignments").append(option);
    }
}

function getPFP() {
  var current = gapi.auth2.getAuthInstance().currentUser.get().getBasicProfile();
  console.log(current.getGivenName());
  document.querySelector(".logo").innerHTML = "Hi " + current.getGivenName() + "!";
  document.querySelector("#PFP").src = "" + current.getImageUrl() + "";
  console.log(current.getImageUrl());
  console.log(current.getEmail());
}

function drop(id) {
    var ob = document.getElementById(id);
    ob.classList.toggle("active");
    alert($(".active").style.height);
    // alert(o.innerHTML);
}

function showrep() {
  var list = {};
  list.class = $('#classes').find('option:selected').text();
  list.assign = $('#assignments').find('option:selected').text();
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8000/teacher",
    data: JSON.stringify(list),
    dataType: 'json'
  }).done(function(data) {
      var nn = String(data.name).replace("-", " ");
      let student = `
      <li onclick="drop('${data.name}')" class="person">
      <h2 class="name">${nn}</h2>
      <div class="f-info">
          <h2 class="attenspan">${data.attenspan} secs</h2>
          <h2 class="turns">${data['times-turned-num']} Turns</h2>
      </div>
      </li>
      <ul id="${data.name}" class="person-info">
      </ul>`;
      $(".name-list").append(student);
      for (x in data['times-turned']) {
        let sInfo = `<li class="info">${data['times-turned'][x]} </li>`;
        $(String("#" + data.name)).append(sInfo);
      }
      // console.log(data);
      // alert(data);
      console.log("DONE");
  });
  var container = document.querySelector(".content");
  var report = document.querySelector(".report");
  container.style.display = "none";
  report.style.display = "block";
}


