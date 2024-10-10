const loader = document.querySelector('.loader');
const submit = document.querySelector('.button-submit');

const usuario = document.querySelector('#usuario');
const video = document.querySelector('#video');

const spanUsuario = document.querySelector('.usuario');
const spanVideo = document.querySelector('.video');

document.addEventListener('submit', e => {
    let validador = true;

    spanUsuario.innerHTML = ''
    spanCurso.innerHTML = ''

    if(usuario.value == 'Escolha o usuário'){
        e.preventDefault();
        spanUsuario.innerHTML = 'O campo acima não pode ficar vazio!';
        validador = false;
    }
    if(video.value == 'Escolha o vídeo'){
        e.preventDefault();
        spanVideo.innerHTML = 'O campo acima não pode ficar vazio!';
        validador = false;
    }

    if(validador){
        loader.classList.add('desocultar');
        submit.classList.add('ocultar');
    }
})