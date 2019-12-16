let canvas = document.getElementById("mapbox");
canvas.setAttribute(
  "style",
  "position: absolute;background-color: rgba(0, 0, 0, 0.2) !important;border-radius: 15px !important;"
);

// margin-left:-600px;
// margin-top:-115px;left: 50%; top: 20%;
let ctx = canvas.getContext("2d");
console.log("canvas init");

//alert("enter x, y");

point = [];
mouseLocation = { mouseX: 0, mouseY: 0 };

let floor0 = new Image();
floor0.src = "../static/floor0.png";
let floor1 = new Image();
floor1.src = "../static/floor1.png";

let floor = "0";
let section = localStorage.getItem("aisle");

let marker = new Image();
marker.src = "../static/marker.png";

let sectionbtn = document.getElementById("section-btn");
sectionbtn.onclick = getSection;

let floor0btn = document.getElementById("floor0btn");
floor0btn.onclick = function() {
  if (floor === "1") point = [];
  floor = "0";
  updateCanvas();
};
let floor1btn = document.getElementById("floor1btn");
floor1btn.onclick = function() {
  if (floor === "0") point = [];
  floor = "1";
  updateCanvas();
};

function getFloor() {
  floor = document.getElementById("floor").value;

  updateCanvas();
}

function getSection() {
  //section = document.getElementById("section").value;
  section = localStorage.getItem("aisle");

  if (1 <= parseInt(section) && parseInt(section) <= 7) {
    floor = "0";
    updateCanvas();
  }
  if (8 <= parseInt(section) && parseInt(section) <= 15) {
    floor = "1";
    updateCanvas();
  }

  switch (section) {
    case "1":
      point = [177, 308];
      break;
    case "2":
      point = [372, 304];
      break;
    case "3":
      point = [482, 308];
      break;
    case "4":
      point = [120, 91];
      break;
    case "5":
      point = [543, 92];
      break;
    case "6":
      point = [115, 555];
      break;
    case "7":
      point = [538, 555];
      break;
    case "8":
      point = [76, 79];
      break;
    case "9":
      point = [571, 77];
      break;
    case "10":
      point = [66, 177];
      break;
    case "11":
      point = [579, 176];
      break;
    case "12":
      point = [136, 342];
      break;
    case "13":
      point = [503, 431];
      break;
    case "14":
      point = [104, 537];
      break;
    case "15":
      point = [515, 538];
      break;
  }

  updateCanvas();
}

function mouseMove(e) {
  if (e.offsetX) {
    mouseLocation.mouseX = e.offsetX;
    mouseLocation.mouseY = e.offsetY;
  } else if (e.layerX) {
    mouseLocation.mouseX = e.layerX;
    mouseLocation.mouseY = e.layerY;
  }

  /* do something with mouseX/mouseY */

  updateCanvas();
}

function mouseClick(e) {
  point = [mouseLocation.mouseX, mouseLocation.mouseY];
  updateCanvas();
}

function updateCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (floor === "0") ctx.drawImage(floor0, 0, 0, canvas.width, canvas.height);
  if (floor === "1") ctx.drawImage(floor1, 0, 0, canvas.width, canvas.height);

  // points.forEach(point => {
  //   // ctx.beginPath();
  //   // ctx.arc(point[0], point[1], 5, 2 * Math.PI, false);
  //   // ctx.fillStyle = "red";
  //   // ctx.fill();
  //   ctx.drawImage(marker, point[0] - 15, point[1] - 30);
  // });

  ctx.drawImage(marker, point[0] - 15, point[1] - 30);

  ctx.fillStyle = "black";
  ctx.fillRect(mouseLocation.mouseX, mouseLocation.mouseY, 1, 1);
  ctx.fillRect(mouseLocation.mouseX, mouseLocation.mouseY - 10, 1, 20);
  ctx.fillRect(mouseLocation.mouseX - 10, mouseLocation.mouseY, 20, 1);
}

function welcome() {
  ctx.rect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "rgba(0,0,0,0.5)";
  ctx.fill();

  ctx.font = "40px Candara";
  ctx.fillStyle = "white";
  ctx.textAlign = "center";
  ctx.fillText("Welcome to VCETMart", canvas.width / 2, canvas.height / 2);
}

// canvas.addEventListener("mousemove", event => {
//   mouseMove(event);
//   //console.log("mouse event");
// });

// canvas.addEventListener("mousedown", event => {
//   mouseClick(event);
//   //console.log("mouse click");
//   console.log(mouseLocation.mouseX, " ", mouseLocation.mouseY);
// });
updateCanvas();
welcome();
