import React from "react";
import TypingCard from "@/components/TypingCard";
const About = () => {
  const cardContent = `
    <p>您的赞赏，是我不断前进的动力！</p>
  `;
  return (
    <div className="app-container">
      <TypingCard title="关于作者" source={cardContent} />
    </div>
  );
};

export default About;
