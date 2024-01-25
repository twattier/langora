import './Profile.css'

//Source : https://codepen.io/Hyperplexed/pen/dydJGZM

export default function Profile(content) {
  const Wrap = ({ content }) => <div>{content}</div>
  return (
    <div speech-bubble pleft abottom style={{ '--bbColor': '#484a9b' }}>
      <Wrap />
    </div>
  )
}
