import Box from '@mui/material/Box'
import Grid from '@mui/material/Grid'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'

import ListItemSearch from './atoms/ListItemSearch'
import ListItemSource from './atoms/ListItemSource'

export default function QueryResults(props) {
  const { similarities } = props

  return (
    <Grid container spacing={1} sx={{ pr: 2 }} alignItems="stretch">
      <Grid item sm={12} md={6}>
        <Stack spacing={1}>
          <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
            Searches
          </Typography>
          <Divider />
          <Box sw={{ width: '100%' }}>
            {similarities.searches?.map((sim) => (
              <ListItemSearch search={sim.search} />
            ))}
          </Box>
        </Stack>
      </Grid>
      <Grid item sm={12} md={6}>
        <Stack spacing={1}>
          <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
            Sources
          </Typography>
          <Divider />
          <Box sw={{ width: '100%' }}>
            {similarities.sources?.map((sim) => (
              <ListItemSource source={sim.source} />
            ))}
          </Box>
        </Stack>
      </Grid>
    </Grid>
  )
}
