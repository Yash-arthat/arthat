const express = require('express');
const nodemailer = require('nodemailer');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

app.post('/send', (req, res) => {
    const { username, email, contactNo, description } = req.body;

    // Create a transporter using your email service (e.g., Gmail)
    const transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: 'yash.gautam@arthat.org', // Replace with your email
            pass: 'kennjqcypxpjxzki'   // Replace with your email password or an app password
        }
    });

    // Email options
    const mailOptions = {
        from: email, // The user's email
        to: 'your-email@gmail.com', // Your email address where you want to receive the form data
        subject: 'New Contact Us Form Submission',
        text: `You have a new contact us form submission:\n\nUsername: ${username}\nEmail: ${email}\nContact No: ${contactNo}\nDescription: ${description}`
    };

    // Send the email
    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.log(error);
            return res.status(500).json({ message: 'Internal Server Error' });
        } else {
            console.log('Email sent: ' + info.response);
            return res.status(200).json({ message: 'Email sent successfully' });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
