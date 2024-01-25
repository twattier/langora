import './SpeechBubbles.css'

//Source : https://codepen.io/MarkBoots/pen/RwLPXgJ

export default function SpeechBubbles(content) {
  return (
    <div speech-bubble pleft abottom style={{'--bbColor':'#484a9b'}}>
      <content/>
    </div>
  )
}
