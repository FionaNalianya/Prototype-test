import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import SimpleMDE from 'react-simplemde-editor';
import 'easymde/dist/easymde.min.css';
import axios from 'axios';
// import markdownfile from '../components/test.md';
import markdownfile from "../components/background.md";
import { Button } from 'semantic-ui-react';

const MarkdownEditor = () => {
  const [markdown, setMarkdown] = useState('');
  const [isEditing, setIsEditing] = useState(false);

  // Function to fetch the markdown file
  const fetchMarkdown = async () => {
    try {
      const response = await axios.get(markdownfile);
      setMarkdown(response.data);
    } catch (error) {
      console.error('Error fetching markdown:', error);
    }
  };

  // Load the markdown file when the component mounts
  useEffect(() => {
    fetchMarkdown();
  }, []);

  // Toggle between view and edit mode
  const toggleEditMode = () => {
    setIsEditing(!isEditing);
  };

  // Handle markdown change
  const handleMarkdownChange = (value) => {
    setMarkdown(value);
  };

  return (
    <div>
        <Button primary onClick={toggleEditMode}>
        {isEditing ? 'Save Changes' : 'Edit Markdown'}
      </Button>
      {isEditing ? (
        <SimpleMDE value={markdown} onChange={handleMarkdownChange} />
      ) : (
        <ReactMarkdown>{markdown}</ReactMarkdown>
      )}
      
    </div>
  );
};

export default MarkdownEditor;