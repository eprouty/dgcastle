import copy
import os
import pickle
import unittest
from unittest.mock import patch

from dgcastle import dgcastle
from dgcastle.exceptions import IncompleteException
from dgcastle.exceptions import ValidationException
from dgcastle.handlers.challonge import Challonge

TEST_TOURNAMENT = pickle.loads(b'\x80\x03}q\x00(X\x02\x00\x00\x00idq\x01J.X6\x00X\x04\x00\x00\x00nameq\x02X\x07\x00\x00\x00DG Testq\x03X\x03\x00\x00\x00urlq\x04X\x08\x00\x00\x00mwtmsdjsq\x05X\x0b\x00\x00\x00descriptionq\x06X\x1b\x00\x00\x00This is just a test bracketq\x07X\x0f\x00\x00\x00tournament-typeq\x08X\x12\x00\x00\x00single eliminationq\tX\n\x00\x00\x00started-atq\ncdatetime\ndatetime\nq\x0bC\n\x07\xe1\x06\t\x0e,\x13\x00\x00\x00q\x0cciso8601.iso8601\nFixedOffset\nq\rJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\x0e\x87q\x0fRq\x10}q\x11(X\x1a\x00\x00\x00_FixedOffset__offset_hoursq\x12J\xfc\xff\xff\xffX\x1c\x00\x00\x00_FixedOffset__offset_minutesq\x13K\x00X\x14\x00\x00\x00_FixedOffset__offsetq\x14cdatetime\ntimedelta\nq\x15J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\x16Rq\x17X\x12\x00\x00\x00_FixedOffset__nameq\x18h\x0eub\x86q\x19Rq\x1aX\x0c\x00\x00\x00completed-atq\x1bh\x0bC\n\x07\xe1\x06\t\x10\x14$\x00\x00\x00q\x1ch\rJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\x1d\x87q\x1eRq\x1f}q (h\x12J\xfc\xff\xff\xffh\x13K\x00h\x14h\x15J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q!Rq"h\x18h\x1dub\x86q#Rq$X\x17\x00\x00\x00require-score-agreementq%\x89X\x1e\x00\x00\x00notify-users-when-matches-openq&\x88X\n\x00\x00\x00created-atq\'h\x0bC\n\x07\xe1\x06\t\x0e+\x10\x00\x00\x00q(h\rJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q)\x87q*Rq+}q,(h\x12J\xfc\xff\xff\xffh\x13K\x00h\x14h\x15J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q-Rq.h\x18h)ub\x86q/Rq0X\n\x00\x00\x00updated-atq1h\x0bC\n\x07\xe1\x06\t\x10\x14$\x00\x00\x00q2h\rJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q3\x87q4Rq5}q6(h\x12J\xfc\xff\xff\xffh\x13K\x00h\x14h\x15J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q7Rq8h\x18h3ub\x86q9Rq:X\x05\x00\x00\x00stateq;X\x08\x00\x00\x00completeq<X\x0b\x00\x00\x00open-signupq=\x89X%\x00\x00\x00notify-users-when-the-tournament-endsq>\x88X\x0e\x00\x00\x00progress-meterq?KdX\r\x00\x00\x00quick-advanceq@\x89X\x16\x00\x00\x00hold-third-place-matchqA\x89X\x10\x00\x00\x00pts-for-game-winqBcdecimal\nDecimal\nqCX\x03\x00\x00\x000.0qD\x85qERqFX\x10\x00\x00\x00pts-for-game-tieqGhCX\x03\x00\x00\x000.0qH\x85qIRqJX\x11\x00\x00\x00pts-for-match-winqKhCX\x03\x00\x00\x001.0qL\x85qMRqNX\x11\x00\x00\x00pts-for-match-tieqOhCX\x03\x00\x00\x000.5qP\x85qQRqRX\x0b\x00\x00\x00pts-for-byeqShCX\x03\x00\x00\x001.0qT\x85qURqVX\x0c\x00\x00\x00swiss-roundsqWK\x00X\x07\x00\x00\x00privateqX\x89X\t\x00\x00\x00ranked-byqYX\n\x00\x00\x00match winsqZX\x0b\x00\x00\x00show-roundsq[\x88X\n\x00\x00\x00hide-forumq\\\x89X\x13\x00\x00\x00sequential-pairingsq]\x89X\x12\x00\x00\x00accept-attachmentsq^\x89X\x13\x00\x00\x00rr-pts-for-game-winq_hCX\x03\x00\x00\x000.0q`\x85qaRqbX\x13\x00\x00\x00rr-pts-for-game-tieqchCX\x03\x00\x00\x000.0qd\x85qeRqfX\x14\x00\x00\x00rr-pts-for-match-winqghCX\x03\x00\x00\x001.0qh\x85qiRqjX\x14\x00\x00\x00rr-pts-for-match-tieqkhCX\x03\x00\x00\x000.5ql\x85qmRqnX\x0e\x00\x00\x00created-by-apiqo\x89X\r\x00\x00\x00credit-cappedqp\x89X\x08\x00\x00\x00categoryqqNX\n\x00\x00\x00hide-seedsqr\x89X\x11\x00\x00\x00prediction-methodqsK\x00X\x15\x00\x00\x00predictions-opened-atqtNX\x10\x00\x00\x00anonymous-votingqu\x89X\x18\x00\x00\x00max-predictions-per-userqvK\x01X\n\x00\x00\x00signup-capqwNX\x07\x00\x00\x00game-idqxK@X\x12\x00\x00\x00participants-countqyK\x08X\x14\x00\x00\x00group-stages-enabledqz\x89X!\x00\x00\x00allow-participant-match-reportingq{\x88X\x05\x00\x00\x00teamsq|\x89X\x11\x00\x00\x00check-in-durationq}NX\x08\x00\x00\x00start-atq~NX\x16\x00\x00\x00started-checking-in-atq\x7fNX\n\x00\x00\x00tie-breaksq\x80X\x05\x00\x00\x00\n    q\x81X\t\x00\x00\x00locked-atq\x82NX\x08\x00\x00\x00event-idq\x83NX$\x00\x00\x00public-predictions-before-start-timeq\x84\x89X\x06\x00\x00\x00rankedq\x85\x89X\x15\x00\x00\x00grand-finals-modifierq\x86NX\x1a\x00\x00\x00predict-the-losers-bracketq\x87\x89X\x04\x00\x00\x00spamq\x88NX\x03\x00\x00\x00hamq\x89NX\x12\x00\x00\x00description-sourceq\x8aX\x1b\x00\x00\x00This is just a test bracketq\x8bX\t\x00\x00\x00subdomainq\x8cNX\x12\x00\x00\x00full-challonge-urlq\x8dX\x1d\x00\x00\x00http://challonge.com/mwtmsdjsq\x8eX\x0e\x00\x00\x00live-image-urlq\x8fX!\x00\x00\x00http://challonge.com/mwtmsdjs.svgq\x90X\x0b\x00\x00\x00sign-up-urlq\x91NX\x18\x00\x00\x00review-before-finalizingq\x92\x88X\x15\x00\x00\x00accepting-predictionsq\x93\x89X\x13\x00\x00\x00participants-lockedq\x94\x88X\t\x00\x00\x00game-nameq\x95X\t\x00\x00\x00Disc Golfq\x96X\x16\x00\x00\x00participants-swappableq\x97\x89X\x10\x00\x00\x00team-convertableq\x98\x89X\x19\x00\x00\x00group-stages-were-startedq\x99\x89u.')
TEST_MATCH_INDEX = pickle.loads(b'\x80\x03]q\x00(}q\x01(X\x02\x00\x00\x00idq\x02J\xef\xd0Z\x05X\r\x00\x00\x00tournament-idq\x03J.X6\x00X\x05\x00\x00\x00stateq\x04X\x08\x00\x00\x00completeq\x05X\n\x00\x00\x00player1-idq\x06J\xfc.c\x03X\n\x00\x00\x00player2-idq\x07J\x0e/c\x03X\x17\x00\x00\x00player1-prereq-match-idq\x08NX\x17\x00\x00\x00player2-prereq-match-idq\tNX\x1d\x00\x00\x00player1-is-prereq-match-loserq\n\x89X\x1d\x00\x00\x00player2-is-prereq-match-loserq\x0b\x89X\t\x00\x00\x00winner-idq\x0cJ\xfc.c\x03X\x08\x00\x00\x00loser-idq\rJ\x0e/c\x03X\n\x00\x00\x00started-atq\x0ecdatetime\ndatetime\nq\x0fC\n\x07\xe1\x06\t\x0e,\x13\x00\x00\x00q\x10ciso8601.iso8601\nFixedOffset\nq\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\x12\x87q\x13Rq\x14}q\x15(X\x1a\x00\x00\x00_FixedOffset__offset_hoursq\x16J\xfc\xff\xff\xffX\x1c\x00\x00\x00_FixedOffset__offset_minutesq\x17K\x00X\x14\x00\x00\x00_FixedOffset__offsetq\x18cdatetime\ntimedelta\nq\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\x1aRq\x1bX\x12\x00\x00\x00_FixedOffset__nameq\x1ch\x12ub\x86q\x1dRq\x1eX\n\x00\x00\x00created-atq\x1fh\x0fC\n\x07\xe1\x06\t\x0e,\x13\x00\x00\x00q h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q!\x87q"Rq#}q$(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q%Rq&h\x1ch!ub\x86q\'Rq(X\n\x00\x00\x00updated-atq)h\x0fC\n\x07\xe1\x06\t\x0e-\r\x00\x00\x00q*h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q+\x87q,Rq-}q.(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q/Rq0h\x1ch+ub\x86q1Rq2X\n\x00\x00\x00identifierq3X\x01\x00\x00\x00Aq4X\x0e\x00\x00\x00has-attachmentq5\x89X\x05\x00\x00\x00roundq6K\x01X\r\x00\x00\x00player1-votesq7NX\r\x00\x00\x00player2-votesq8NX\x08\x00\x00\x00group-idq9NX\x10\x00\x00\x00attachment-countq:NX\x0e\x00\x00\x00scheduled-timeq;NX\x08\x00\x00\x00locationq<NX\x0b\x00\x00\x00underway-atq=NX\x08\x00\x00\x00optionalq>\x89X\x08\x00\x00\x00rushb-idq?NX\x0c\x00\x00\x00completed-atq@h\x0fC\n\x07\xe1\x06\t\x0e-\r\x00\x00\x00qAh\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00qB\x87qCRqD}qE(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87qFRqGh\x1chBub\x86qHRqIX\x14\x00\x00\x00suggested-play-orderqJK\x01X\x1a\x00\x00\x00prerequisite-match-ids-csvqKNX\n\x00\x00\x00scores-csvqLX\x03\x00\x00\x002-0qMu}qN(h\x02J\xf0\xd0Z\x05h\x03J.X6\x00h\x04X\x08\x00\x00\x00completeqOh\x06J\xff.c\x03h\x07J\x00/c\x03h\x08Nh\tNh\n\x89h\x0b\x89h\x0cJ\x00/c\x03h\rJ\xff.c\x03h\x0eh\x0fC\n\x07\xe1\x06\t\x0e,\x13\x00\x00\x00qPh\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00qQ\x87qRRqS}qT(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87qURqVh\x1chQub\x86qWRqXh\x1fh\x0fC\n\x07\xe1\x06\t\x0e,\x13\x00\x00\x00qYh\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00qZ\x87q[Rq\\}q](h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q^Rq_h\x1chZub\x86q`Rqah)h\x0fC\n\x07\xe1\x06\t\x10\x123\x00\x00\x00qbh\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00qc\x87qdRqe}qf(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87qgRqhh\x1chcub\x86qiRqjh3X\x01\x00\x00\x00Bqkh5\x89h6K\x01h7Nh8Nh9Nh:Nh;Nh<Nh=Nh>\x89h?Nh@h\x0fC\n\x07\xe1\x06\t\x10\x123\x00\x00\x00qlh\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00qm\x87qnRqo}qp(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87qqRqrh\x1chmub\x86qsRqthJK\x02hKNhLX\x03\x00\x00\x002-4quu}qv(h\x02J\xf1\xd0Z\x05h\x03J.X6\x00h\x04X\x08\x00\x00\x00completeqwh\x06J\xfd.c\x03h\x07J\x02/c\x03h\x08Nh\tNh\n\x89h\x0b\x89h\x0cJ\x02/c\x03h\rJ\xfd.c\x03h\x0eh\x0fC\n\x07\xe1\x06\t\x0e,\x13\x00\x00\x00qxh\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00qy\x87qzRq{}q|(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q}Rq~h\x1chyub\x86q\x7fRq\x80h\x1fh\x0fC\n\x07\xe1\x06\t\x0e,\x13\x00\x00\x00q\x81h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\x82\x87q\x83Rq\x84}q\x85(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\x86Rq\x87h\x1ch\x82ub\x86q\x88Rq\x89h)h\x0fC\n\x07\xe1\x06\t\x10\x13\r\x00\x00\x00q\x8ah\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\x8b\x87q\x8cRq\x8d}q\x8e(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\x8fRq\x90h\x1ch\x8bub\x86q\x91Rq\x92h3X\x01\x00\x00\x00Cq\x93h5\x89h6K\x01h7Nh8Nh9Nh:Nh;Nh<Nh=Nh>\x89h?Nh@h\x0fC\n\x07\xe1\x06\t\x10\x13\r\x00\x00\x00q\x94h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\x95\x87q\x96Rq\x97}q\x98(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\x99Rq\x9ah\x1ch\x95ub\x86q\x9bRq\x9chJK\x03hKNhLX\x03\x00\x00\x000-2q\x9du}q\x9e(h\x02J\xf2\xd0Z\x05h\x03J.X6\x00h\x04X\x08\x00\x00\x00completeq\x9fh\x06J\xfe.c\x03h\x07J\x01/c\x03h\x08Nh\tNh\n\x89h\x0b\x89h\x0cJ\xfe.c\x03h\rJ\x01/c\x03h\x0eh\x0fC\n\x07\xe1\x06\t\x0e,\x13\x00\x00\x00q\xa0h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xa1\x87q\xa2Rq\xa3}q\xa4(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xa5Rq\xa6h\x1ch\xa1ub\x86q\xa7Rq\xa8h\x1fh\x0fC\n\x07\xe1\x06\t\x0e,\x13\x00\x00\x00q\xa9h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xaa\x87q\xabRq\xac}q\xad(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xaeRq\xafh\x1ch\xaaub\x86q\xb0Rq\xb1h)h\x0fC\n\x07\xe1\x06\t\x10\x134\x00\x00\x00q\xb2h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xb3\x87q\xb4Rq\xb5}q\xb6(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xb7Rq\xb8h\x1ch\xb3ub\x86q\xb9Rq\xbah3X\x01\x00\x00\x00Dq\xbbh5\x89h6K\x01h7Nh8Nh9Nh:Nh;Nh<Nh=Nh>\x89h?Nh@h\x0fC\n\x07\xe1\x06\t\x10\x134\x00\x00\x00q\xbch\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xbd\x87q\xbeRq\xbf}q\xc0(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xc1Rq\xc2h\x1ch\xbdub\x86q\xc3Rq\xc4hJK\x04hKNhLX\x03\x00\x00\x009-8q\xc5u}q\xc6(h\x02J\xf3\xd0Z\x05h\x03J.X6\x00h\x04X\x08\x00\x00\x00completeq\xc7h\x06J\xfc.c\x03h\x07J\x00/c\x03h\x08J\xef\xd0Z\x05h\tJ\xf0\xd0Z\x05h\n\x89h\x0b\x89h\x0cJ\xfc.c\x03h\rJ\x00/c\x03h\x0eh\x0fC\n\x07\xe1\x06\t\x10\x123\x00\x00\x00q\xc8h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xc9\x87q\xcaRq\xcb}q\xcc(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xcdRq\xceh\x1ch\xc9ub\x86q\xcfRq\xd0h\x1fh\x0fC\n\x07\xe1\x06\t\x0e,\x13\x00\x00\x00q\xd1h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xd2\x87q\xd3Rq\xd4}q\xd5(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xd6Rq\xd7h\x1ch\xd2ub\x86q\xd8Rq\xd9h)h\x0fC\n\x07\xe1\x06\t\x10\x14\x0c\x00\x00\x00q\xdah\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xdb\x87q\xdcRq\xdd}q\xde(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xdfRq\xe0h\x1ch\xdbub\x86q\xe1Rq\xe2h3X\x01\x00\x00\x00Eq\xe3h5\x89h6K\x02h7Nh8Nh9Nh:Nh;Nh<Nh=Nh>\x89h?Nh@h\x0fC\n\x07\xe1\x06\t\x10\x14\x0c\x00\x00\x00q\xe4h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xe5\x87q\xe6Rq\xe7}q\xe8(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xe9Rq\xeah\x1ch\xe5ub\x86q\xebRq\xechJK\x05hKX\x11\x00\x00\x0089837807,89837808q\xedhLX\x03\x00\x00\x001-0q\xeeu}q\xef(h\x02J\xf4\xd0Z\x05h\x03J.X6\x00h\x04X\x08\x00\x00\x00completeq\xf0h\x06J\x02/c\x03h\x07J\xfe.c\x03h\x08J\xf1\xd0Z\x05h\tJ\xf2\xd0Z\x05h\n\x89h\x0b\x89h\x0cJ\xfe.c\x03h\rJ\x02/c\x03h\x0eh\x0fC\n\x07\xe1\x06\t\x10\x134\x00\x00\x00q\xf1h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xf2\x87q\xf3Rq\xf4}q\xf5(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xf6Rq\xf7h\x1ch\xf2ub\x86q\xf8Rq\xf9h\x1fh\x0fC\n\x07\xe1\x06\t\x0e,\x13\x00\x00\x00q\xfah\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xfb\x87q\xfcRq\xfd}q\xfe(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xffRr\x00\x01\x00\x00h\x1ch\xfbub\x86r\x01\x01\x00\x00Rr\x02\x01\x00\x00h)h\x0fC\n\x07\xe1\x06\t\x10\x14\x02\x00\x00\x00r\x03\x01\x00\x00h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00r\x04\x01\x00\x00\x87r\x05\x01\x00\x00Rr\x06\x01\x00\x00}r\x07\x01\x00\x00(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87r\x08\x01\x00\x00Rr\t\x01\x00\x00h\x1cj\x04\x01\x00\x00ub\x86r\n\x01\x00\x00Rr\x0b\x01\x00\x00h3X\x01\x00\x00\x00Fr\x0c\x01\x00\x00h5\x89h6K\x02h7Nh8Nh9Nh:Nh;Nh<Nh=Nh>\x89h?Nh@h\x0fC\n\x07\xe1\x06\t\x10\x14\x02\x00\x00\x00r\r\x01\x00\x00h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00r\x0e\x01\x00\x00\x87r\x0f\x01\x00\x00Rr\x10\x01\x00\x00}r\x11\x01\x00\x00(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87r\x12\x01\x00\x00Rr\x13\x01\x00\x00h\x1cj\x0e\x01\x00\x00ub\x86r\x14\x01\x00\x00Rr\x15\x01\x00\x00hJK\x06hKX\x11\x00\x00\x0089837809,89837810r\x16\x01\x00\x00hLX\x03\x00\x00\x003-4r\x17\x01\x00\x00u}r\x18\x01\x00\x00(h\x02J\xf5\xd0Z\x05h\x03J.X6\x00h\x04X\x08\x00\x00\x00completer\x19\x01\x00\x00h\x06J\xfc.c\x03h\x07J\xfe.c\x03h\x08J\xf3\xd0Z\x05h\tJ\xf4\xd0Z\x05h\n\x89h\x0b\x89h\x0cJ\xfe.c\x03h\rJ\xfc.c\x03h\x0eh\x0fC\n\x07\xe1\x06\t\x10\x14\x0c\x00\x00\x00r\x1a\x01\x00\x00h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00r\x1b\x01\x00\x00\x87r\x1c\x01\x00\x00Rr\x1d\x01\x00\x00}r\x1e\x01\x00\x00(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87r\x1f\x01\x00\x00Rr \x01\x00\x00h\x1cj\x1b\x01\x00\x00ub\x86r!\x01\x00\x00Rr"\x01\x00\x00h\x1fh\x0fC\n\x07\xe1\x06\t\x0e,\x13\x00\x00\x00r#\x01\x00\x00h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00r$\x01\x00\x00\x87r%\x01\x00\x00Rr&\x01\x00\x00}r\'\x01\x00\x00(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87r(\x01\x00\x00Rr)\x01\x00\x00h\x1cj$\x01\x00\x00ub\x86r*\x01\x00\x00Rr+\x01\x00\x00h)h\x0fC\n\x07\xe1\x06\t\x10\x14\x1d\x00\x00\x00r,\x01\x00\x00h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00r-\x01\x00\x00\x87r.\x01\x00\x00Rr/\x01\x00\x00}r0\x01\x00\x00(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87r1\x01\x00\x00Rr2\x01\x00\x00h\x1cj-\x01\x00\x00ub\x86r3\x01\x00\x00Rr4\x01\x00\x00h3X\x01\x00\x00\x00Gr5\x01\x00\x00h5\x89h6K\x03h7Nh8Nh9Nh:Nh;Nh<Nh=Nh>\x89h?Nh@h\x0fC\n\x07\xe1\x06\t\x10\x14\x1d\x00\x00\x00r6\x01\x00\x00h\x11J\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00r7\x01\x00\x00\x87r8\x01\x00\x00Rr9\x01\x00\x00}r:\x01\x00\x00(h\x16J\xfc\xff\xff\xffh\x17K\x00h\x18h\x19J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87r;\x01\x00\x00Rr<\x01\x00\x00h\x1cj7\x01\x00\x00ub\x86r=\x01\x00\x00Rr>\x01\x00\x00hJK\x07hKX\x11\x00\x00\x0089837811,89837812r?\x01\x00\x00hLX\x03\x00\x00\x001-3r@\x01\x00\x00ue.')
TEST_PARTICIPANTS_INDEX = pickle.loads(b'\x80\x03]q\x00(}q\x01(X\x02\x00\x00\x00idq\x02J\xfc.c\x03X\r\x00\x00\x00tournament-idq\x03J.X6\x00X\x04\x00\x00\x00nameq\x04X\x01\x00\x00\x00Aq\x05X\x04\x00\x00\x00seedq\x06K\x01X\x06\x00\x00\x00activeq\x07\x88X\n\x00\x00\x00created-atq\x08cdatetime\ndatetime\nq\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00q\nciso8601.iso8601\nFixedOffset\nq\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\x0c\x87q\rRq\x0e}q\x0f(X\x1a\x00\x00\x00_FixedOffset__offset_hoursq\x10J\xfc\xff\xff\xffX\x1c\x00\x00\x00_FixedOffset__offset_minutesq\x11K\x00X\x14\x00\x00\x00_FixedOffset__offsetq\x12cdatetime\ntimedelta\nq\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\x14Rq\x15X\x12\x00\x00\x00_FixedOffset__nameq\x16h\x0cub\x86q\x17Rq\x18X\n\x00\x00\x00updated-atq\x19h\tC\n\x07\xe1\x06\t\x0e,\x0f\x00\x00\x00q\x1ah\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\x1b\x87q\x1cRq\x1d}q\x1e(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\x1fRq h\x16h\x1bub\x86q!Rq"X\x0c\x00\x00\x00invite-emailq#NX\n\x00\x00\x00final-rankq$K\x02X\x04\x00\x00\x00miscq%NX\x04\x00\x00\x00iconq&NX\x0f\x00\x00\x00on-waiting-listq\'\x89X\r\x00\x00\x00invitation-idq(NX\x08\x00\x00\x00group-idq)NX\r\x00\x00\x00checked-in-atq*NX\x12\x00\x00\x00challonge-usernameq+NX \x00\x00\x00challonge-email-address-verifiedq,NX\t\x00\x00\x00removableq-\x89X%\x00\x00\x00participatable-or-invitation-attachedq.\x89X\x0e\x00\x00\x00confirm-removeq/\x88X\x12\x00\x00\x00invitation-pendingq0\x89X*\x00\x00\x00display-name-with-invitation-email-addressq1h\x05X\n\x00\x00\x00email-hashq2NX\x08\x00\x00\x00usernameq3NX\x0c\x00\x00\x00display-nameq4h\x05X$\x00\x00\x00attached-participatable-portrait-urlq5NX\x0c\x00\x00\x00can-check-inq6\x89X\n\x00\x00\x00checked-inq7\x89X\r\x00\x00\x00reactivatableq8\x89X\r\x00\x00\x00check-in-openq9\x89X\x10\x00\x00\x00group-player-idsq:NX\x13\x00\x00\x00has-irrelevant-seedq;\x89u}q<(h\x02J\xfd.c\x03h\x03J.X6\x00h\x04X\x01\x00\x00\x00Bq=h\x06K\x02h\x07\x88h\x08h\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00q>h\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q?\x87q@RqA}qB(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87qCRqDh\x16h?ub\x86qERqFh\x19h\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00qGh\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00qH\x87qIRqJ}qK(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87qLRqMh\x16hHub\x86qNRqOh#Nh$K\x05h%Nh&Nh\'\x89h(Nh)Nh*Nh+Nh,Nh-\x89h.\x89h/\x88h0\x89h1h=h2Nh3Nh4h=h5Nh6\x89h7\x89h8\x89h9\x89h:Nh;\x89u}qP(h\x02J\xfe.c\x03h\x03J.X6\x00h\x04X\x01\x00\x00\x00CqQh\x06K\x03h\x07\x88h\x08h\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00qRh\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00qS\x87qTRqU}qV(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87qWRqXh\x16hSub\x86qYRqZh\x19h\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00q[h\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\\\x87q]Rq^}q_(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q`Rqah\x16h\\ub\x86qbRqch#Nh$K\x01h%Nh&Nh\'\x89h(Nh)Nh*Nh+Nh,Nh-\x89h.\x89h/\x88h0\x89h1hQh2Nh3Nh4hQh5Nh6\x89h7\x89h8\x89h9\x89h:Nh;\x89u}qd(h\x02J\xff.c\x03h\x03J.X6\x00h\x04X\x01\x00\x00\x00Dqeh\x06K\x04h\x07\x88h\x08h\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00qfh\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00qg\x87qhRqi}qj(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87qkRqlh\x16hgub\x86qmRqnh\x19h\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00qoh\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00qp\x87qqRqr}qs(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87qtRquh\x16hpub\x86qvRqwh#Nh$K\x05h%Nh&Nh\'\x89h(Nh)Nh*Nh+Nh,Nh-\x89h.\x89h/\x88h0\x89h1heh2Nh3Nh4heh5Nh6\x89h7\x89h8\x89h9\x89h:Nh;\x89u}qx(h\x02J\x00/c\x03h\x03J.X6\x00h\x04X\x01\x00\x00\x00Eqyh\x06K\x05h\x07\x88h\x08h\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00qzh\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q{\x87q|Rq}}q~(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\x7fRq\x80h\x16h{ub\x86q\x81Rq\x82h\x19h\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00q\x83h\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\x84\x87q\x85Rq\x86}q\x87(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\x88Rq\x89h\x16h\x84ub\x86q\x8aRq\x8bh#Nh$K\x03h%Nh&Nh\'\x89h(Nh)Nh*Nh+Nh,Nh-\x89h.\x89h/\x88h0\x89h1hyh2Nh3Nh4hyh5Nh6\x89h7\x89h8\x89h9\x89h:Nh;\x89u}q\x8c(h\x02J\x01/c\x03h\x03J.X6\x00h\x04X\x01\x00\x00\x00Fq\x8dh\x06K\x06h\x07\x88h\x08h\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00q\x8eh\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\x8f\x87q\x90Rq\x91}q\x92(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\x93Rq\x94h\x16h\x8fub\x86q\x95Rq\x96h\x19h\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00q\x97h\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\x98\x87q\x99Rq\x9a}q\x9b(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\x9cRq\x9dh\x16h\x98ub\x86q\x9eRq\x9fh#Nh$K\x05h%Nh&Nh\'\x89h(Nh)Nh*Nh+Nh,Nh-\x89h.\x89h/\x88h0\x89h1h\x8dh2Nh3Nh4h\x8dh5Nh6\x89h7\x89h8\x89h9\x89h:Nh;\x89u}q\xa0(h\x02J\x02/c\x03h\x03J.X6\x00h\x04X\x01\x00\x00\x00Gq\xa1h\x06K\x07h\x07\x88h\x08h\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00q\xa2h\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xa3\x87q\xa4Rq\xa5}q\xa6(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xa7Rq\xa8h\x16h\xa3ub\x86q\xa9Rq\xaah\x19h\tC\n\x07\xe1\x06\t\x0e+/\x00\x00\x00q\xabh\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xac\x87q\xadRq\xae}q\xaf(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xb0Rq\xb1h\x16h\xacub\x86q\xb2Rq\xb3h#Nh$K\x03h%Nh&Nh\'\x89h(Nh)Nh*Nh+Nh,Nh-\x89h.\x89h/\x88h0\x89h1h\xa1h2Nh3Nh4h\xa1h5Nh6\x89h7\x89h8\x89h9\x89h:Nh;\x89u}q\xb4(h\x02J\x0e/c\x03h\x03J.X6\x00h\x04X\x01\x00\x00\x00Hq\xb5h\x06K\x08h\x07\x88h\x08h\tC\n\x07\xe1\x06\t\x0e+8\x00\x00\x00q\xb6h\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xb7\x87q\xb8Rq\xb9}q\xba(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xbbRq\xbch\x16h\xb7ub\x86q\xbdRq\xbeh\x19h\tC\n\x07\xe1\x06\t\x0e,\x0f\x00\x00\x00q\xbfh\x0bJ\xfc\xff\xff\xffK\x00X\x06\x00\x00\x00-04:00q\xc0\x87q\xc1Rq\xc2}q\xc3(h\x10J\xfc\xff\xff\xffh\x11K\x00h\x12h\x13J\xff\xff\xff\xffJ@\x19\x01\x00K\x00\x87q\xc4Rq\xc5h\x16h\xc0ub\x86q\xc6Rq\xc7h#Nh$K\x05h%Nh&Nh\'\x89h(Nh)Nh*Nh+Nh,Nh-\x89h.\x89h/\x88h0\x89h1h\xb5h2Nh3Nh4h\xb5h5Nh6\x89h7\x89h8\x89h9\x89h:Nh;\x89ue.')

class TestChallongeImport(unittest.TestCase):
    def setUp(self):
        self.dgcastle = dgcastle.DGCastle(testDb="TestChallonge")
        os.environ['CHALLONGE_API'] = 'test,test'

    def tearDown(self):
        del(self.dgcastle)

    def test_import(self):
        t = None
        with patch('challonge.tournaments') as mock_tournaments:
            mock_tournaments.show.return_value = TEST_TOURNAMENT
            with patch('challonge.participants') as mock_participants:
                mock_participants.index.return_value = TEST_PARTICIPANTS_INDEX
                with patch('challonge.matches') as mock_matches:
                    mock_matches.index.return_value = TEST_MATCH_INDEX
                
                    t = self.dgcastle.challonge_import(1)

        self.assertEqual(len(t.participants), 8)
        self.assertEqual(len(t.matches), 7)

    def test_incompleteBracket(self):
        with patch('challonge.tournaments') as mock_tournaments:
            ret_val = copy.deepcopy(TEST_TOURNAMENT)
            ret_val['state'] = 'not complete'
            mock_tournaments.show.return_value = ret_val

            self.assertRaises(IncompleteException, self.dgcastle.challonge_import, 1)

    def test_incorrectResultsData(self):
        with patch('challonge.tournaments') as mock_tournaments:
            mock_tournaments.show.return_value = TEST_TOURNAMENT
            with patch('challonge.participants') as mock_participants:
                mock_participants.index.return_value = TEST_PARTICIPANTS_INDEX
                with patch('challonge.matches') as mock_matches:
                    ret_val = copy.deepcopy(TEST_MATCH_INDEX)
                    ret_val[0]['scores-csv'] = '1-0,2-1'
                    mock_matches.index.return_value = ret_val

                    self.assertRaises(ValidationException, self.dgcastle.challonge_import, 1)