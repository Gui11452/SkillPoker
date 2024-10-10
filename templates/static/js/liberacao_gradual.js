const loader = document.querySelector('.loader');
const submit = document.querySelector('.button-submit');

const usuario = document.querySelector('#usuario');
const curso = document.querySelector('#curso');
const tempo = document.querySelector('#tempo');

const spanUsuario = document.querySelector('.usuario');
const spanCurso = document.querySelector('.curso');
const spanTempo = document.querySelector('.tempo');

document.addEventListener('submit', e => {
    let validador = true;

    spanUsuario.innerHTML = ''
    spanCurso.innerHTML = ''
    spanTempo.innerHTML = ''

    if(usuario.value == 'Escolha o usuário'){
        e.preventDefault();
        spanUsuario.innerHTML = 'O campo acima não pode ficar vazio!';
        validador = false;
    }
    if(curso.value == 'Escolha o vídeo'){
        e.preventDefault();
        spanCurso.innerHTML = 'O campo acima não pode ficar vazio!';
        validador = false;
    }
    if(tempo.value == 'Escolha o tempo'){
        e.preventDefault();
        spanTempo.innerHTML = 'O campo acima não pode ficar vazio!';
        validador = false;
    }

    if(validador){
        loader.classList.add('desocultar');
        submit.classList.add('ocultar');
    }
})