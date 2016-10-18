import random

class Miscellaneous(object):
  def _print(self, lst):
    print(random.choice(lst))

  def welcome_banner(self):
    self._print([
      "Project 1 or whatever - IT384",
      "Welcome to the NHK! - IT384",
      "ASCII art makes the code run faster, right? - IT384",
      "MAJ Hutchison is not a softie! - IT384",
      "The files are in the computer. - IT384",
      "The enemy's gate is down! - IT384",
    ])
  
  def cut_sling_load(self):
    self._print([
      "\n\nBreak, Break, Break! - FM24-19",
      "\n\nI'm done like a potato in the oven!",
      "\n\nWhat happened? Did you see an evil bit?... (RFC 3514)",
      "\n\nCan you hear me MAJ Tom?"
    ])

  def exit_msg(self):
    self._print([
      "\n\nAir Assault!\n" + \
      "   ______.........--=T=--.........______\n" + \
      "      .             |:|\n" + \
      " :-. //           /\"\"\"\"\"\"-.\n" + \
      " ': '-._____..--\"\"(\"\"\"\"\"\"()`---.__\n" + \
      "  /:   _..__   ''  \":\"\"\"\"'[] |\"\"`\\\n" + \
      "  ': :'     `-.IT384_:._     '\"\"\"\" :\n" + \
      "   ::          '--=:____:.___....-\"\n" + \
      "                     O\"       O\"",
      
      "\n\n                                                 :::\n" +
      "                                             :: :::.\n" +
      "                       \\/,                    .:::::\n" +
      "           \\),          \\`-._                 :::888\n" +
      "           /\\            \\   `-.             ::88888\n" +
      "          /  \\            | .(                ::88\n" +
      "         /,.  \\           ; ( `              .:8888\n" +
      "            ), \\         / ;``               :::888\n" +
      "           /_   \\     __/_(_                  :88\n" +
      "             `. ,`..-'      `-._    \\  /      :8\n" +
      "               )__ `.           `._ .\\/.\n" +
      "              /   `. `             `-._______m         _,\n" +
      "  ,-=====-.-;'      IT384      ,  ___________/ _,-_,'\"`/__,-.\n" +
      " C   =--   ;                   `.`._    V V V       -=-'\"#==-._\n" +
      ":,  \\     ,|      UuUu _,......__   `-.__A_A_ -. ._ ,--._ \",`` `-\n" +
      "||  |`---' :    uUuUu,'          `'--...____/   `\" `\".   `\n" +
      "|`  :       \\   UuUu:\n" +
      ":  /         \\   UuUu`-._           TROGDOR\n" +
      " \\(_          `._  uUuUu `-.            the\n" +
      " (_3             `._  uUu   `._       BURNINATOR\n" +
      "                    ``-._      `.\n" +
      "                         `-._    `.\n" +
      "                             `.    \\\n" +
      "                               )   ;\n" +
      "                              /   /\n" +
      "               `.        |\\ ,'   /\n" +
      "                 \",_A_/\\-| `   ,'\n" +
      "                   `--..,_|_,-'\\\n" +
      "                          |     \\\n" +
      "                          |      \__\n" +
      "                          |__",
      
      "\n\n                             ,|\n" +
      "                           //|                              ,|\n" +
      "                         //,/                             -~ |\n" +
      "                       // / |                         _-~   /  ,\n" +
      "                     /'/ / /                       _-~   _/_-~ |\n" +
      "                    ( ( / /'                   _ -~     _-~ ,/'\n" +
      "                     \\~\\/'/|             __--~~__--\\ _-~  _/,\n" +
      "             ,,)))))));, \\/~-_     __--~~  --~~  __/~  _-~ /\n" +
      "          __))))))))))))));,>/\\   /        __--~~  \\-~~ _-~\n" +
      "         -\\(((((''''(((((((( >~\/     --~~   __--~' _-~ ~|\n" +
      "--==//////((''  .     `)))))), /     ___---~~  ~~\\~~__--~ \n" +
      "        ))| @    ;-.     (((((/           __--~~~'~~/\n" +
      "        ( `|    /  )      )))/      ~~~~~__\\__---~~__--~~--_\n" +
      "           |   |   |       (/      ---~~~/__-----~~  ,;::'  \\         ,\n" +
      "           o_);   ;        /      ----~~/           \\,-~~~\\  |       /|\n" +
      "                 ; IT384  (      ---~~/         `:::|      |;|      < >\n" +
      "                |   _      `----~~~~'      /      `:|       \\;\\_____// \n" +
      "          ______/\\/~    |                 /        /         ~------~\n" +
      "        /~;;.____/;;'  /          ___----(   `;;;/\n" +
      "       / //  _;______;'------~~~~~    |;;/\\    /\n" +
      "      //  | |                        /  |  \\;;,\\\n" +
      "     (<_  | ;                      /',/-----'  _>\n" +
      "      \\_| ||_                     //~;~~~~~~~~~ \n" +
      "          `\\_|                   (,~~ \n" +
      "                                  \\~\\ \n" +
      "                                   ~~\n"
    ])
Misc = Miscellaneous()
