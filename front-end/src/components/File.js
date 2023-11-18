import React, { useState } from 'react';

const File = () => {
  const [resume, setResume] = useState(null);
  const [skills, setSkills] = useState([]);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];

    if (file) {
      const formData = new FormData();
      formData.append('resume', file);

      try {
        const response = await fetch('YOUR_API_ENDPOINT', {
          method: 'POST',
          headers: {
            'Authorization': 'JOVzLPoZPJHxEJ4uOpjdLKmqNYNfPWMW',
          },
          body: formData,
        });

        if (response.ok) {
          const parsedData = await response.json();
          // Assuming the API response contains skills data
          setSkills(parsedData.skills);
        } else {
          console.error('Failed to parse resume');
        }
      } catch (error) {
        console.error('Error parsing resume:', error);
      }
    }
  };

  return (
    <div>
      <input type="file" accept=".pdf,.doc,.docx" onChange={handleFileUpload} />
      {skills.length > 0 && (
        <div>
          <h2>Extracted Skills:</h2>
          <ul>
            {skills.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default File;