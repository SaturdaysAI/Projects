let contNav = document.querySelector(".flaying");
let butNav = contNav.querySelectorAll("nav ul li");
let secNav = contNav.querySelectorAll("section div");
let h4Nav = contNav.querySelectorAll("section ");

let colors = ['#FFBE00', '#FFA100', '#FF8600', '#FF5D00', '#F84400', '#E62F00', '#CE0045', '#D51570', '#982B95', '#7C1797', '#4C008F', '#8B6ACE', '#595DC7', '#2C67C9', '#0054A3', '#068495', '#009283', '#008455', '#287121', '#54AB00'];

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

butNav[0].addEventListener('click', (e)=>  {
    secNav[0].classList.toggle("on");
    secNav[1].classList.remove("on");
});

butNav[1].addEventListener('click', (e)=>  {
    secNav[1].classList.toggle("on");
    secNav[0].classList.remove("on");
});

for(let i=0; i < h4Nav.length; i++){
    h4Nav[i].addEventListener('mouseenter', (e)=>  {
        document.documentElement.style.setProperty('--bColorR', colors[getRandomInt(colors.length)]);
    });
}

