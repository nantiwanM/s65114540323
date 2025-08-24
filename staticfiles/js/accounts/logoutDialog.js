// JavaScript สำหรับควบคุมการแสดง/ซ่อนกล่องไดอะล็อก

document.addEventListener('DOMContentLoaded', function() {

    const logoutBtns = document.querySelectorAll('.logoutBtn')
    const logoutDialog = document.getElementById('logoutDialog');
    const cancelBtn = document.getElementById('cancelBtn');

    // วนลูปผ่านทุกปุ่ม ที่มี class="logoutBtn" ก่อนที่จะเพิ่ม event listener
     logoutBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            logoutDialog.classList.remove('hidden');
        });
    });

    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
            logoutDialog.classList.add('hidden');
        });
    }
});