class MentalHealthController {
    static async getHomePage(req, res) {
        try {
            res.render('index', { title: 'Mental Health Assistant' });
        } catch (error) {
            res.status(500).send('Server Error');
        }
    }

    // Additional methods for handling other routes can be added here
}

export default MentalHealthController;