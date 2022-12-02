var req = new XMLHttpRequest(); //建立物件
req.open(
  "GET",
  "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json",
  true
); //請求 使用同步
req.send();

var re1 = /臺北市\s+(.*)/;
var re2 = /https:\/\/.*?jpg/;
var create_allcontent = function (element, attributes, text = null) {
  var newnode = document.createElement(element);
  Object.keys(attributes).forEach((attr) => {
    newnode.setAttribute(attr, attributes[attr]);
  });
  if (text) {
    var textnode = document.createTextNode(text);
    newnode.appendChild(textnode);
  }
  return newnode;
};
function getalldata(Object) {
  var data = JSON.parse(Object.responseText);
  var all_Data = [];
  for (let i = 0; i < data["result"]["results"].length; i++) {
    var single_data = {};
    for (const key of ["stitle", "longitude", "xbody", "address", "file"]) {
      try {
        if (key === "address") {
          data["result"]["results"][i][key].match(re1);
          single_data[key] = RegExp.$1;
          continue;
        }
        if (key === "file") {
          single_data[key] = data["result"]["results"][i][key].match(re2)[0];
          continue;
        }
      } catch {
        single_data[key] = "something error";
        continue;
      }
      single_data[key] = data["result"]["results"][i][key];
    }
    all_Data.push(single_data);
  }
  console.log(all_Data);
  return all_Data;
}
var create_box = function (array) {
  array.forEach((x) => {
    var boxcontainer = document.querySelector(".l-boxcontainer");
    var box = create_allcontent("div", { class: "box box--bgcolor" });
    var box_img_div = create_allcontent("div", { class: "box__img" });
    var box_img = create_allcontent("img", {
      class: "u-img-cover",
      alt: "Lago di Braies",
      src: x["file"],
    });
    var box__content = create_allcontent("div", { class: "box__content" });
    var box__title = create_allcontent(
      "h3",
      { class: "t3 box__title" },
      (text = x["stitle"])
    );
    var box__p = create_allcontent(
      "p",
      { class: "t4 box__p" },
      (text = x["xbody"])
    );
    var box__a = create_allcontent(
      "div",
      { class: "t4 js-box__btn" },
      (text = "Load more")
    );
    var box__icons = create_allcontent("div", { class: "box__icons" });
    var text_grey = create_allcontent(
      "span",
      { class: "t5 text-grey" },
      (text = x["address"])
    );
    var location = create_allcontent("i", {
      class: "fa-solid fa-location-dot",
    });
    var text_grey2 = create_allcontent("span", { class: "t4 text-grey" });
    var user = create_allcontent("i", { class: "fas fa-user text-red" });

    boxcontainer.appendChild(box);
    box.appendChild(box_img_div);
    box_img_div.appendChild(box_img);
    box.appendChild(box__content);
    box__content.appendChild(box__title);
    box__content.appendChild(box__p);
    box__content.appendChild(box__a);
    box__content.appendChild(box__icons);
    box__icons.appendChild(location);
    box__icons.appendChild(text_grey);
  });
};
req.onload = () => {
  var all_Data = getalldata(req);
  create_box(all_Data);
  loadmoreimgbtn();
  loadimgcontext();
};
function loadmoreimgbtn() {
  var btn = document.querySelector(".js-btn");
  var boxshow = 8;
  var allbox = document.querySelectorAll(".box");
  btn.addEventListener("click", () => {
    try {
      if (boxshow <= allbox.length) {
        for (i = 0; i < boxshow + 8; i++) {
          allbox[i].style.display = "inline-block";
        }
        boxshow = boxshow + 8;
      } else {
        console.log(123);
      }
    } catch {
      x = btn.childNodes[0];
      btn.removeChild(x);
      var endtextnode = document.createTextNode("END");
      btn.appendChild(endtextnode);
    }
  });
}

function loadimgcontext() {
  var btn = document.querySelectorAll(".js-box__btn");
  var img_comtent_p = document.querySelectorAll(".box__p");
  //這個dict是拿來紀錄各img請求狀態 整除2就會是展開 不整除則會收回
  const check = {};
  // 如果只用 i 不是用 let i，你會發現事件裡面的i都是58,這是因為用function切分變數
  for (let i = 0; i < btn.length; i++) {
    btn[i].addEventListener("click", () => {
      var remembernum = `imgnum${i}`;
      if (check.hasOwnProperty(remembernum)) {
        check[remembernum] = check[remembernum] + 1;
      } else {
        check[remembernum] = 0;
      }
      if (check[remembernum] % 2 === 0) {
        img_comtent_p[i].style.display = "block";
      } else {
        img_comtent_p[i].style.display = "-webkit-box";
      }
      console.log(check[remembernum]);
    });
  }
}
