import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Accordion from '@mui/material/Accordion'
import AccordionSummary from '@mui/material/AccordionSummary'
import AccordionDetails from '@mui/material/AccordionDetails'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'

import { DisplayLines } from '../../utils/display'
import { Link } from '@mui/material'

export default function ListItemDocument(props) {
  const { document } = props

  return (
    <Stack justifyContent="center">
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Stack
            direction="row"
            justifyContent="flex-start"
            alignItems="center"
            sx={{ height: 34, mt: 1, mb: 1 }}
          >
            <Typography variant="body2" color="secondary" sx={{ mr: 2 }}>
              {(document.score_total * 100).toFixed(2)}%
            </Typography>
            <img
              src={`http://www.google.com/s2/favicons?domain=${document.source.site}`}
              alt={document.source.site}
              width="20"
              height="20"
            />
            <Stack>
              <Typography variant="body2" sx={{ pl: 1 }}>
                {document.source.title}
              </Typography>
              <Typography variant="body2" sx={{ pl: 1 }}>
                &#8227;{` ${document.source_text.title}`}
              </Typography>
            </Stack>
          </Stack>
        </AccordionSummary>
        <AccordionDetails>
          <Box>
            <Stack direction="row">
              <Link
                underline="none"
                variant="caption"
                href={`/knowledges/sources/${document.source.id}`}
              >
                Source 
              </Link>
              <Typography variant="caption">{`  :  `}</Typography>
              <Link
                underline="none"
                variant="caption"
                href={document.source.url}
                target="_blank"
              >
                {document.source.site}
              </Link>
            </Stack>
            <DisplayLines text={document.source_text.text} variant="body2" />
          </Box>
        </AccordionDetails>
      </Accordion>
    </Stack>
  )
}
