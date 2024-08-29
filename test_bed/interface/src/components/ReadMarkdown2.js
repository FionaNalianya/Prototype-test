import React,{ useEffect, useState } from 'react'
import readmePath from "../components/background.md";
import { marked } from "marked";

function ReadMarkdown2() {
    const [data, setData] = useState("");
    useEffect(() => {
      fetch(readmePath)
        .then((response) => {
          return response.text();
        })
        .then((text) => {
          setData(marked(text));
        });
    }, []);
    return (
      <React.Fragment>
        <article dangerouslySetInnerHTML={{ __html: data }} />
      </React.Fragment>
    );
}

export default ReadMarkdown2