import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'

import { ContentBox } from '../utils/style/component'
import ListItemSearch from './atoms/ListItemSearch'
import ListItemSource from './atoms/ListItemSource'

export default function QueryResults(props) {
  const { similarities } = props

  return (
    <ContentBox>
      <Stack spacing={1} sx={{ m: 1 }}>
        <Typography
          variant="subtitle1"
          color="primary"
          sx={{ fontWeight: 'bold' }}
        >
          Similarities results for : {similarities.query}
        </Typography>
        <Divider />
        <Stack direction="row" spacing={2}>
          <Stack spacing={2} sx={{ m: 1, width: '100%' }}>
            <Stack >
              <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                Searches
              </Typography>
              <Divider />
              {similarities.searches?.map((sim) => (
                <ListItemSearch search={sim.search} />
              ))}
            </Stack>
            <Stack sx={{ m: 1, width: '100%' }}>
              <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                Sources
              </Typography>
              <Divider />
              {similarities.sources?.map((sim) => (
                <ListItemSource source={sim.source} />
              ))}
            </Stack>
          </Stack>
          <Box>More command</Box>
        </Stack>
      </Stack>
    </ContentBox>
  )
}
