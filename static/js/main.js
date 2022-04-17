const genderLang = {
  "Woman": "Женщина", "Man": "Мужчина"
}
const emotionLang = {
  'angry': "Злость",
  'disgust': "Отвращение",
  'fear': "Страх",
  'happy': "Радость",
  'sad': "Грусть",
  'surprise': "Удивление",
  'neutral': "Нейтральная"
}
const raceLang = {
  "asian": "Азиатская",
  "white": "Европеоидная",
  "middle eastern": "Восточная",
  "indian": "Индийская",
  "latino": "Латиноамериканская",
  "black": "Афроамериканская"
}
function getPicture(backend, actions) {
  const canvas = document.createElement("canvas");
  const landmarkChk = document.getElementById("landmarkChk").checked;
  const facemeshChk = document.getElementById("facemeshChk").checked;
  if (actions.length == 0) {
    document.getElementById("result").classList.toggle("hide", true);
  } else {
    document.getElementById("result").classList.toggle("hide", false);
  }
  if (landmarkChk || facemeshChk) {
    document.getElementById("detection").classList.toggle("hide", false);
  } else {
    document.getElementById("detection").classList.toggle("hide", true);
  }
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d')
    .drawImage(video, 0, 0, canvas.width, canvas.height);
  const dataURL = canvas.toDataURL();
  try {
    const response = fetch(window.location.href + "send_image", {
      method: 'POST',
      body: JSON.stringify(
        {
          "image": dataURL.replace(/\s+/g, ''),
          "actions": actions,
          "backend": backend,
          "landmarks": landmarkChk,
          "facemesh": facemeshChk
        }),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then((res) => {
      res.json().then((val) => {
        var noface = document.getElementById("not-find-face");
        var age = document.getElementById("age");
        var emotion = document.getElementById("dominant_emotion");
        var race = document.getElementById("dominant_race");
        var gender = document.getElementById("gender");
        if (val.code === 0) {
          if (val.err === "No face")
            noface.classList.toggle("hide", false);
          return;
        }
        noface.classList.toggle("hide", true)
        age.innerText = actions.includes("age") ? "Возраст: " + val.age : "";
        emotion.innerText = actions.includes("emotion") ? "Эмоция: " + emotionLang[val.dominant_emotion] : "";
        race.innerText = actions.includes("race") ? "Расса: " + raceLang[val.dominant_race] : "";
        gender.innerText = actions.includes("gender") ? "Пол: " + genderLang[val.gender] : "";
        if (val.image != undefined) {
          let img = document.getElementById("detection-container");
          document.getElementById("detection").src = val.image;
          img.classList.toggle("hide", false);
        }
      })
    });
  } catch (error) {
    console.error('Ошибка:', error);
  }
}
var actions = [1, 2, 3, 4]
function sendloop() {
  setTimeout(() => {
    var actions = [];
    var backend = document.getElementById("backend").value;
    var types = ["age", "gender", "emotion", "race"];
    for (let i = 0; i < types.length; i++) {
      if (document.getElementById(types[i] + "Chk").checked == true) {
        actions.push(types[i]);
      }
    }
    getPicture(backend, actions);
    sendloop();
    console.log(actions.length)
  }, (actions.length > 1 ? actions.length * 500 : 50))
}
function start() {
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
  var button = document.getElementById("showBtn");
  var showingDataContainer = document.getElementById("showingDataContainer");
  var landing = document.getElementById("landing");
  showingDataContainer.classList.toggle("hide");
  landing.classList.toggle("hide");
}