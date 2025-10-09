{
   "date": "2025-10-09T14:10:20-05:00",
   "draft": false,
   "title": "But what if I want to close the lid?",
   "tags" : [
      "homelab",
      "technical"
   ]
}

![Laptop lid](laptop-lid.webp)

I recently turned an old laptop into a home server, and that experience made me think of [the picture above](https://www.reddit.com/r/ProgrammerHumor/comments/z8qfrd/startups_be_like/) [^1]. If I want my server/laptop quietly sitting in a closet or under my desk, I will have to shut the lid. How can I do that without turning the computer off?

Fortunately, all Linux distributions that run `systemd` [^2] make this problem pretty easy to solve.

In a fresh Ubuntu server install, open `/etc/systemd/logind.conf` and make a few changes. Uncomment `HandleLidSwitch`, `HandleLidSwitchExternalPower`, and `HandleLidSwitchDocked`, and set the value of each to `ignore`.

```
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
```

What are we doing here? We're just telling `systemd-logind`, the `systemd` daemon that manages user sessions and "seats" (where a "seat" is a collection of hardware assigned to users), that we don't want it to do anything when it sees a `SW_LID` event appear on the `/dev/input/event*` device file.

Once these changes are made, you can apply the new `systemd-logind` configuration file with
{{< highlight bash >}}
$ sudo service systemd-logind restart
{{< /highlight >}}

Congrats! Now you can close the lid on your self-hosted Linux servers at your new startup.

## Sources
 - [AskUbuntu](https://askubuntu.com/questions/15520/how-can-i-tell-ubuntu-to-do-nothing-when-i-close-my-laptop-lid)


 [^2]: And maybe even the ones that don't! But that is outside the scope of this article.
 [^1]: I used to think r/ProgrammerHumor was funny as a freshman in undergrad, but as I learned more, the humor revealed itself to be a little too surface-level and a little too "I'm bad at my job" for my liking.