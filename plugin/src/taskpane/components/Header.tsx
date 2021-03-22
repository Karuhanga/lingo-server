import * as React from "react";

export interface HeaderProps {
  title: string;
  logo: string;
  message: string;
}

export default class Header extends React.Component<HeaderProps> {
  render() {
    const { title, logo, message } = this.props;

    return (
      <section className="ms-welcome__header ms-bgColor-neutralLighter ms-u-fadeIn500" style={{paddingTop: "30px", paddingBottom: "15px"}}>
        <img width="60" height="60" src={logo} alt={title} title={title} />
        <h1 className="ms-fontWeight-semilight ms-fontColor-neutralPrimary">{message}</h1>
      </section>
    );
  }
}
