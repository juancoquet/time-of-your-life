const tooltips = document.querySelectorAll('.all-tooltips');
const fullDiv = document.querySelector('.calendar');
const calendar = document.querySelector('.calendar');

window.addEventListener('DOMContentLoaded', contentPosition);
// window.addEventListener('resize', contentPosition);
// window.addEventListener('DOMContentLoaded', buildModal);
// window.addEventListener('DOMContentLoaded', tapPresentWeek);
window.addEventListener('DOMContentLoaded', calculatePositionOnTap);
window.addEventListener('DOMContentLoaded', calculatePositionOnHover);


function contentPosition(){
    tooltips.forEach(tooltip => {
        const event = tooltip.querySelector('.week.event');
        const content = tooltip.querySelector('.tooltip-content');
        const arrow = tooltip.querySelector('.arrow');


        content.style.left = event.offsetWidth/2 - content.offsetWidth/2 + 'px';
        content.style.top = event.offsetHeight*3.5 + 'px';
        
        tooltipBoundaries = content.getBoundingClientRect();
        calendarBoundaies = calendar.getBoundingClientRect();

        if(tooltipBoundaries.right > calendarBoundaies.right){
            arrow.style.borderBottomColor = 'transparent';
            arrow.style.borderLeftColor = '#F8F1F1';
            arrow.style.top = arrow.offsetHeight/2 + content.offsetHeight/2 + 'px';
            arrow.style.left = content.offsetWidth + arrow.offsetWidth/2 + 'px';
            
            content.style.left = -content.offsetWidth - arrow.offsetWidth + 'px';
            content.style.top = -content.offsetHeight/2 + event.offsetHeight/2 + 'px';
        }

        if(tooltipBoundaries.left < calendarBoundaies.left){
            arrow.style.borderBottomColor = 'transparent';
            arrow.style.borderRightColor = '#F8F1F1';
            arrow.style.top = arrow.offsetHeight/2 + content.offsetHeight/2 + 'px';
            arrow.style.left = -arrow.offsetWidth/2 + 'px';
            
            content.style.left = event.offsetWidth + arrow.offsetWidth + 'px';
            content.style.top = -content.offsetHeight/2 + event.offsetHeight/2 + 'px';
        }
        
    })
}

function calculatePositionOnTap() {
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('touchstart', function calculate() {
            console.log('calculating');

            const event = tooltip.querySelector('.week.event');
            const content = tooltip.querySelector('.tooltip-content');
            const arrow = tooltip.querySelector('.arrow');
            
            tooltipBoundaries = content.getBoundingClientRect();
            calendarBoundaies = calendar.getBoundingClientRect();
            console.log(tooltipBoundaries)

            if(tooltipBoundaries.right > calendarBoundaies.right){
                arrow.style.borderBottomColor = 'transparent';
                arrow.style.borderLeftColor = '#F8F1F1';
                arrow.style.top = arrow.offsetHeight/2 + content.offsetHeight/2 + 'px';
                arrow.style.left = content.offsetWidth + arrow.offsetWidth/2 + 'px';
                
                content.style.left = -content.offsetWidth - arrow.offsetWidth + 'px';
                content.style.top = -content.offsetHeight/2 + event.offsetHeight/2 + 'px';
            }

            if(tooltipBoundaries.left < calendarBoundaies.left){
                arrow.style.borderBottomColor = 'transparent';
                arrow.style.borderRightColor = '#F8F1F1';
                arrow.style.top = arrow.offsetHeight/2 + content.offsetHeight/2 + 'px';
                arrow.style.left = -arrow.offsetWidth/2 + 'px';
                
                content.style.left = event.offsetWidth + arrow.offsetWidth + 'px';
                content.style.top = -content.offsetHeight/2 + event.offsetHeight/2 + 'px';
            }
        })
    })
}

function calculatePositionOnHover() {
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function calculate() {
            console.log('calculating');

            const event = tooltip.querySelector('.week.event');
            const content = tooltip.querySelector('.tooltip-content');
            const arrow = tooltip.querySelector('.arrow');
            
            tooltipBoundaries = content.getBoundingClientRect();
            calendarBoundaies = calendar.getBoundingClientRect();
            console.log(tooltipBoundaries)

            if(tooltipBoundaries.right > calendarBoundaies.right){
                arrow.style.borderBottomColor = 'transparent';
                arrow.style.borderLeftColor = '#F8F1F1';
                arrow.style.top = arrow.offsetHeight/2 + content.offsetHeight/2 + 'px';
                arrow.style.left = content.offsetWidth + arrow.offsetWidth/2 + 'px';
                
                content.style.left = -content.offsetWidth - arrow.offsetWidth + 'px';
                content.style.top = -content.offsetHeight/2 + event.offsetHeight/2 + 'px';
            }

            if(tooltipBoundaries.left < calendarBoundaies.left){
                arrow.style.borderBottomColor = 'transparent';
                arrow.style.borderRightColor = '#F8F1F1';
                arrow.style.top = arrow.offsetHeight/2 + content.offsetHeight/2 + 'px';
                arrow.style.left = -arrow.offsetWidth/2 + 'px';
                
                content.style.left = event.offsetWidth + arrow.offsetWidth + 'px';
                content.style.top = -content.offsetHeight/2 + event.offsetHeight/2 + 'px';
            }
        })
    })
}

const eventWeeks = document.querySelectorAll('.week.event');
const closeBtns = document.querySelectorAll('.close-button');

// function buildModal() {
//     eventWeeks.forEach(eventWeek => {
//         eventWeek.addEventListener('touchend', function() {
//             var modal = document.querySelector('#modal-bg-' + eventWeek.id);
//             modal.style.display = 'flex';
            
//             var closeBtn = modal.querySelector('.close-button')
//             closeBtn.addEventListener('touchend', function() {
//                 modal.style.display = 'none'
//             })
            
//         })
//     })
// }

// const presentWeek = document.querySelectorAll('.week.present');

// function tapPresentWeek() {
//     presentWeek.forEach(week => {
//         week.addEventListener('touchend', function tap() {
//             console.log('tapped');


//             week.style.transform = 'scale(2)';
//             week.classList.add('hide-pulse');
//             weekNum = week.querySelector('.week__number');
//             weekNum.style.fontSize = '0.4rem';
//             weekNum.style.visibility = 'visible';



//             setTimeout(function (){
//                 week.removeEventListener('touchend', tap);
//                 document.addEventListener('touchend', function remove() {
//                     console.log('scale down');


//                     week.style.transform = 'scale(1)';
//                     week.classList.remove('hide-pulse')
//                     weekNum.style.fontSize = '0.1rem';
//                     weekNum.style.visibility = 'hidden';


//                     document.removeEventListener('touchend', remove);
//                     week.addEventListener('touchend', tap);
//                 })}, 500);
//         })
//     })
// }