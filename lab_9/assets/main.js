const emailElem = document.getElementById('emailTo');
const subjectElem = document.getElementById('subject');
const messageElem = document.getElementById('message');
const attachmentElem = document.getElementById('attachment');
const submitBtn = document.getElementById('submitBtn');
const statusElem = document.getElementById('emailStatus');

submitBtn.addEventListener('click', (e) => {
  e.preventDefault();

  if (emailElem.value === '' || subjectElem.value === '' || messageElem.value === '') {
    alert('Please fill in all fields');
    return;
  }

  const email = emailElem.value;
  const subject = subjectElem.value;
  const message = messageElem.value;
  const attachment = attachmentElem.files[0];

  const formData = new FormData();
  formData.append('email', email);
  formData.append('subject', subject);
  formData.append('message', message);
  formData.append('attachment', attachment);

  fetch('http://127.0.0.1:5000/api/email', {
    method: 'POST',
    body: formData,
  })
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
    statusElem.textContent = data.message;
    statusElem.classList.add('success');
    statusElem.style.display = 'block';
    cleanForm();
  })
  .catch((error) => {
    console.log(error);
    statusElem.textContent = 'Error sending email'; 
    statusElem.classList.add('error');
    statusElem.style.display = 'block';
    cleanForm();
  });

});

const cleanForm = () => {
  setTimeout(() => {    
    statusElem.classList.remove('success'); 
    statusElem.classList.remove('error'); 
    statusElem.style.display = 'none';

    emailElem.value = '';
    subjectElem.value = '';
    messageElem.value = '';
    attachmentElem.value = '';
  }, 5000);
};