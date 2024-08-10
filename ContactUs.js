import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Navbar from './Navbar';
import Footer from './Footer';
import './ContactUs.css';

const ContactUs = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        contactNo: '',
        description: ''
    });
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitSuccess, setSubmitSuccess] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        fetch('http://localhost:5000/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.ok) {
                setSubmitSuccess(true);
                setFormData({
                    username: '',
                    email: '',
                    contactNo: '',
                    description: ''
                });
            } else {
                // Handle error
            }
            setIsSubmitting(false);
        })
        .catch(error => {
            // Handle error
            setIsSubmitting(false);
        });
    };

    return (
        <>
            <Navbar />
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.5 }}
                className="contact-us-container"
            >
                <div className="form-box">
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="username">User Name:</label>
                            <input
                                type="text"
                                id="username"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                required
                                className="form-control"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="email">Email:</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                required
                                className="form-control emailarea-control"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="contactNo">Contact No.:</label>
                            <input
                                type="text"
                                id="contactNo"
                                name="contactNo"
                                value={formData.contactNo}
                                onChange={handleChange}
                                required
                                className="form-control"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="description">Description:</label>
                            <textarea
                                id="description"
                                name="description"
                                value={formData.description}
                                onChange={handleChange}
                                required
                                className="form-control textarea-control"
                            />
                        </div>
                        <div className="submit-button-container">
                            <button type="submit" className="submit-button" disabled={isSubmitting}>
                                {isSubmitting ? 'Submitting...' : 'Submit'}
                            </button>
                        </div>
                    </form>
                    {submitSuccess && <div className="success-message">Your response has been saved.</div>}
                </div>
            </motion.div>
            <Footer />
        </>
    );
};

export default ContactUs;
