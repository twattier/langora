import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import List from '@mui/material/List'
import ListItemButton from '@mui/material/ListItemButton'
import SearchIcon from '@mui/icons-material/Search'

export default function ListSimilaritySearches(props) {
  const { searches, onSelectSearch } = props

  const handleSelectSearch = (search) => {
    if (onSelectSearch) onSelectSearch(search)
    else window.location.href = '/knowledges/searches/' + search.id
  }

  return (
    <List dense>
      {searches?.map((sim) => (
        <ListItemButton
          sx={{ pt: 0, pb: 0 }}
          onClick={() => handleSelectSearch(sim.search)}
        >
        <Stack
            direction="row"
            justifyContent="flex-start"
            alignItems="center"
            sx={{ height: 24 }}
          >
          <Typography variant="body2" color="secondary" sx={{ mr: 2 }}>
            {(sim.score_query * 100).toFixed(2)}%
          </Typography>
          <SearchIcon sx={{ mr: 1 }} />
          <Typography variant="body2">            
            {`${sim.search.query} [${sim.search.nb_sources}]`}
          </Typography>
          </Stack>
        </ListItemButton>
      ))}
    </List>
  )
}
