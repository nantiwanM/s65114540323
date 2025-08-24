function togglePassword(passwordFieldId, toggleId) {
    let passwordField = document.getElementById(passwordFieldId);
    let toggleIcon = document.getElementById(toggleId);

    if (passwordField.type === 'password') {
        passwordField.type = 'text'; // เปลี่ยนช่องกรอกเป็นแสดงรหัสผ่าน
        toggleIcon.src = toggleIcon.dataset.openIcon; // เปลี่ยนไอคอนเป็นตาลูกเปิด
    } else {
        passwordField.type = 'password'; // เปลี่ยนช่องกรอกเป็นปิดรหัสผ่าน
        toggleIcon.src = toggleIcon.dataset.closeIcon; // เปลี่ยนไอคอนเป็นตาลูกปิด
    }
}
