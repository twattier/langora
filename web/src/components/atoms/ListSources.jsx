import List from '@mui/material/List'
import ListItemButton from '@mui/material/ListItemButton'

import ListItemSource from './ListItemSource'

export default function ListSources(props) {
  const { sources } = props

  return (
    <List dense>
      {sources?.map((source) => (
        <ListItemButton
          sx={{ pt: 0, pb: 0 }}
          onClick={() =>
            (window.location.href = '/knowledges/sources/' + source.id)
          }
        >
          <ListItemSource source={source} />
        </ListItemButton>
      ))}
    </List>
  )
}
