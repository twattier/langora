

export const DisplayLines = (props) => {
    const text = props.text
    return text.split('\n').map((str) => <p>{str}</p>)
  }