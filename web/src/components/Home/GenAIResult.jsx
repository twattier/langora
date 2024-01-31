import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'

import { ContentBox } from '../../utils/style/component'
import ListItemDocument from '../../components/Home/ListItemDocument'
import SimilaritiesResults from '../../components/SimilaritiesResults'
import { DisplayLines } from '../../utils/display'

export default function GenAIResult(props) {
  const { resultGenAI } = props

  return (    
    <ContentBox>
      <Stack spacing={2} sx={{ m: 1, p:1 }}>
        <Box
          sx={{ width: '100%', p: 1, borderRadius: 2, bgcolor: 'white' }}
        >
          <DisplayLines text={resultGenAI.response} />
        </Box>
        <Stack spacing={1}>
          <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
            Documents
          </Typography>
          <Divider />
          {resultGenAI.docs?.map((doc) => (
            <ListItemDocument document={doc} />
          ))}
        </Stack>
        <SimilaritiesResults similarities={resultGenAI.similarities} />
      </Stack>
    </ContentBox>
  )
}
