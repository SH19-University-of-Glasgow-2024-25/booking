import React from 'react';
import '../styles/Header.css';

const Footer: React.FC = () => {
  return (
    <div className="pink-texture text-light mt-4">
      <div className="container py-4 d-md-flex justify-content-between align-items-center">
        <a href="#" className="link-light d-block">
          Organisation name
        </a>
        <p className="mt-2 d-block">
          Organisation Details<br/>
          Such as address
        </p>
      </div>
    </div>
  );
};

export default Footer;
