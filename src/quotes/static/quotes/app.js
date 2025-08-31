document.addEventListener('click', async (ev) => {
  const likeBtn = ev.target.closest('[data-like]');
  const dislikeBtn = ev.target.closest('[data-dislike]');
  if (likeBtn) {
    const id = likeBtn.getAttribute('data-like');
    const resp = await fetch(`/api/quote/${id}/like/`, {method: 'POST', headers: {'X-CSRFToken': getCsrf()}});
    const data = await resp.json();
    document.getElementById(`likes-${id}`).textContent = data.likes;
  }
  if (dislikeBtn) {
    const id = dislikeBtn.getAttribute('data-dislike');
    const resp = await fetch(`/api/quote/${id}/dislike/`, {method: 'POST', headers: {'X-CSRFToken': getCsrf()}});
    const data = await resp.json();
    document.getElementById(`dislikes-${id}`).textContent = data.dislikes;
  }
});

function getCsrf(){
  const m = document.cookie.match(/csrftoken=([^;]+)/);
  return m ? m[1] : '';
}
