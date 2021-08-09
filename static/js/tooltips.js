const tooltips = document.querySelectorAll('.all-tooltips');
const fullDiv = document.querySelector('.calendar');
const calendar = document.querySelector('.calendar');

window.addEventListener('DOMContentLoaded', contentPosition);
window.addEventListener('resize', contentPosition);


function contentPosition(){
    tooltips.forEach(tooltip => {
        const event = tooltip.querySelector('.week.event');
        const content = tooltip.querySelector('.tooltip-content');
        const arrow = tooltip.querySelector('.arrow');


        content.style.left = event.offsetWidth/2 - content.offsetWidth/2 + 'px';
        content.style.top = event.offsetHeight*3 + 'px';
        
        tooltipBoundaries = content.getBoundingClientRect();
        calendarBoundaies = calendar.getBoundingClientRect();

        if(tooltipBoundaries.right > calendarBoundaies.right){
            arrow.style.borderBottomColor = 'transparent';
            arrow.style.borderLeftColor = 'white';
            arrow.style.top = arrow.offsetHeight/2 + content.offsetHeight/2 + 'px';
            arrow.style.left = content.offsetWidth + arrow.offsetWidth/2 + 'px';
            
            content.style.left = -content.offsetWidth - arrow.offsetWidth + 'px';
            content.style.top = -content.offsetHeight/2 + event.offsetHeight/2 + 'px';
        }

        if(tooltipBoundaries.left < calendarBoundaies.left){
            arrow.style.borderBottomColor = 'transparent';
            arrow.style.borderRightColor = 'white';
            arrow.style.top = arrow.offsetHeight/2 + content.offsetHeight/2 + 'px';
            arrow.style.left = -arrow.offsetWidth/2 + 'px';
            
            content.style.left = event.offsetWidth + arrow.offsetWidth + 'px';
            content.style.top = -content.offsetHeight/2 + event.offsetHeight/2 + 'px';
        }
        
    })
}

