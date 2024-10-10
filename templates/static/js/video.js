const abaComunidade = document.querySelectorAll('.aba-comunidade p');
const [botaoComentario, botaoDuvida] = abaComunidade

const comentarios = document.querySelector('.comentarios');
const duvidas = document.querySelector('.duvidas');

const moduloMetricas = document.querySelectorAll('.modulo .modulo-metricas');
const circleProgress = document.querySelectorAll('.modulo .circle-progress');
const circleProgressSvg = document.querySelectorAll('.modulo .circle-progress svg');
const moduloDivH2 = document.querySelectorAll('.modulo>div:nth-of-type(1) h2');
const moduloDivP = document.querySelectorAll('.modulo>div:nth-of-type(1) p');
const moduloDiv = document.querySelectorAll('.modulo>div');

const aulas = document.querySelectorAll('.aulas');

const aulasA = document.querySelectorAll('.aulas a');
const aulasI = document.querySelectorAll('.aulas i');
const aulasP = document.querySelectorAll('.aulas p');

const circle2 = document.querySelectorAll('.circle-progress circle:nth-child(2)');

for(let c = 0; c < circle2.length; c++){
    const porcentagem = parseFloat(circle2[c].getAttribute('porcentagem'));
    if(porcentagem){
        circle2[c].setAttribute('style', `stroke-dashoffset: calc(120 - (120 * ${porcentagem} / 100));`)
    } else{
        circle2[c].setAttribute('style', `display: none;`)
    }
}

for(let i = 0; i < aulasI.length; i++){
    if(aulasI[i].classList.contains('fa-check')){
        aulasI[i].parentElement.style.color = 'green';
        aulasI[i].parentElement.style.fontWeight = 'bold';
    }
}

document.addEventListener('click', e => {

    const el = e.target;

    if(el == botaoComentario){
        botaoComentario.classList.add('selecionado');
        botaoDuvida.classList.remove('selecionado');
        comentarios.classList.remove('ocultar');
        duvidas.classList.remove('desocultar');
    }
    else if(el == botaoDuvida){
        botaoComentario.classList.remove('selecionado');
        botaoDuvida.classList.add('selecionado');
        comentarios.classList.add('ocultar');
        duvidas.classList.add('desocultar');
    }
    
    for(let i = 0; i < moduloMetricas.length; i++){
        if(el == moduloMetricas[i] || el == circleProgress[i] || el == circleProgressSvg[i] || el == moduloDivP[i]
            || el == moduloDivH2[i]
            || el.parentElement.parentElement == moduloDivH2[i]
            || el.parentElement == moduloDivH2[i]
            || el.parentElement == moduloDivP[i]
            || el.parentElement.parentElement == moduloDivP[i]){
            
            if(aulas[i].classList.contains('desocultar')){
                aulas[i].classList.remove('desocultar');
            } else{
                aulas[i].classList.add('desocultar');
            }
        }
    }

    for(let i = 0; i < aulasA.length; i++){
        if(aulasA[i] == el || aulasI[i] == el || aulasP[i] == el){
            if(aulasI[i].classList.contains('fa-lock')){
                e.preventDefault();
                break;
            }
        }
    }

});

document.addEventListener('mouseover', e => {
    const el = e.target;
    for(let i = 0; i < aulasA.length; i++){
        if((aulasA[i] == el || aulasP[i] == el) && aulasI[i].classList.contains('fa-lock')){
            aulasA[i].classList.add('desocultar-after');
        }
    }

});

document.addEventListener('mouseout', e => {
    const el = e.target;
    for(let i = 0; i < aulasA.length; i++){
        if((aulasA[i] == el || aulasP[i] == el) && aulasI[i].classList.contains('fa-lock')){
            aulasA[i].classList.remove('desocultar-after');
        }
    }

});
