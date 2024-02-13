import Typography from '@mui/material/Typography'
import List from '@mui/material/List'
import ListItemButton from '@mui/material/ListItemButton'

import ListItemSource from './ListItemSource'

export default function ListSimilaritySources(props) {
  const { sources, onSelectSource } = props

  const handleSelectSource = (source) => {
    if (onSelectSource) onSelectSource(source)
    else window.location.href = '/knowledges/sources/' + source.id
  }

  return (
    <List dense>
      {sources?.map((sim) => (
        <ListItemButton
          sx={{ pt: 0, pb: 0 }}
          onClick={() => handleSelectSource(sim.source)}
        >
          <Typography variant="body2" color="secondary" sx={{ mr: 2 }}>
            {(sim.score_src * 100).toFixed(2)}%
          </Typography>
          <ListItemSource source={sim.source} />
        </ListItemButton>
      ))}
    </List>
  )
}
