import React, { useState, useEffect } from 'react';
import MarkdownIt from 'markdown-it';
import MdEditor from 'react-markdown-editor-lite';
import 'react-markdown-editor-lite/lib/index.css';
// import markdownfile from '../components/test.md';
import markdownfile from "../components/background.md";
import axios from 'axios';
import { Button } from 'semantic-ui-react';

const MarkdownEditorLite = () => {
  const [markdown, setMarkdown] = useState('');
  const [isEditing, setIsEditing] = useState(false);

  const mdParser = new MarkdownIt();

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
  const handleEditorChange = ({ text }) => {
    setMarkdown(text);
  };

  return (
    <div>
        <Button primary onClick={toggleEditMode}>
        {isEditing ? 'Save Changes' : 'Edit Markdown'}
      </Button>
      {isEditing ? (
        <MdEditor
          value={markdown}
          renderHTML={(text) => mdParser.render(text)}
          onChange={handleEditorChange}
        />
      ) : (
        <div dangerouslySetInnerHTML={{ __html: mdParser.render(markdown) }} />
      )}
    </div>
  );
};

export default MarkdownEditorLite;