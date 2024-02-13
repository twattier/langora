import Grid from '@mui/material/Grid'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'

import { ContentBoxTitle } from '../../utils/style/component'
import ListSimilaritySearches from '../Atoms/ListSimilaritySearches'
import ListSimilaritySources from '../Atoms/ListSimilaritySources'

export default function SimilaritiesResults(props) {
  const { similarities } = props

  return (
    <Grid container spacing={1} sx={{ pr: 2 }} alignItems="stretch">
      <Grid item sm={12} md={6}>
        <Stack spacing={1}>
          <ContentBoxTitle>Searches</ContentBoxTitle>
          <Divider />
          <ListSimilaritySearches searches={similarities.searches} />
        </Stack>
      </Grid>
      <Grid item sm={12} md={6}>
        <Stack spacing={1}>
          <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
            Sources
          </Typography>
          <Divider />
          <ListSimilaritySources sources={similarities.sources}/>          
        </Stack>
      </Grid>
    </Grid>
  )
}
